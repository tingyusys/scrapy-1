# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  17:34
# 文件     :模型剪辑.py
# IDE      :PyCharm

import torch
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit


# 加载YOLOv3-Tiny模型
model = torch.load('yolov3-tiny.pt')

# 置为评估模式
model.eval()

# 剪枝模型
pruned_model = torch.nn.Sequential(
    # 原始模型层
    model.modules()[:5],
    # 剪枝下采样层
    torch.nn.Conv2d(16, 32, 3, 2, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(32, 64, 3, 2, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(64, 128, 3, 2, 1),
    torch.nn.ReLU(),
    # 原始模型层
    model.modules()[12:-1],
    # 剪枝卷积层
    torch.nn.Conv2d(128, 64, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(64, 128, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(128, 64, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(64, 128, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(128, 256, 3, 2, 1),
    torch.nn.ReLU(),
    # 原始模型层
    model.modules()[-8:-3],
    # 剪枝卷积层
    torch.nn.Conv2d(256, 128, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(128, 256, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(256, 128, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(128, 256, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(256, 512, 3, 2, 1),
    torch.nn.ReLU(),
    # 原始模型层
    model.modules()[-3:-1],
    # 剪枝卷积层
    torch.nn.Conv2d(512, 256, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(256, 512, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(512, 256, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(256, 512, 3, 1, 1),
    torch.nn.ReLU(),
    torch.nn.Conv2d(512, 255, 1, 1),
)

# 导出模型为ONNX格式
dummy_input = torch.randn((1, 3, 416, 416))
input_names = ['input']
output_names = ['output']
input_shapes = [(3, 416, 416)]
torch.onnx.export(pruned_model, dummy_input, 'yolov3-tiny.onnx',
                  verbose=True, input_names=input_names, output_names=output_names,
                  opset_version=10, input_shapes=input_shapes)

# 转换为TensorRT的引擎
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
builder = trt.Builder(TRT_LOGGER)
network = builder.create_network(EXPLICIT_BATCH)
parser = trt.OnnxParser(network, TRT_LOGGER)

with open('yolov3-tiny.onnx', 'rb') as model_file:
    onnx_model = model_file.read()

if not parser.parse(onnx_model):
    print('ERROR: Failed to parse ONNX file!')
    for error in range(parser.num_errors):
        print(parser.get_error(error))
    exit()

builder.max_batch_size = 1
builder.max_workspace_size = 1 << 30
engine = builder.build_cuda_engine(network)

# 保存TensorRT引擎
with open('yolov3-tiny.engine', 'wb') as engine_file:
    engine_file.write(engine.serialize())

# 使用TensorRT引擎进行推理
context = engine.create_execution_context()

# 加载图像数据，并进行预处理
image = cv2.imread('image.jpg')
image = cv2.resize(image, (416, 416))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
image /= 255.0
image = np.transpose(image, [2, 0, 1])
image = np.expand_dims(image, axis=0)

# 在GPU上分配内存
input_host = cuda.pagelocked_empty(trt.volume(input_shapes[0]), dtype=np.float32)
output_host = cuda.pagelocked_empty(255 * 13 * 13, dtype=np.float32)

# 在GPU上分配内存
input_device = cuda.mem_alloc(input_host.nbytes)
output_device = cuda.mem_alloc(output_host.nbytes)

# 将数据传输到GPU上
cuda.memcpy_htod_async(input_device, image, stream)

# 进行推理
context.execute_async(1, [int(input_device), int(output_device)], stream.handle)

# 将输出结果从GPU上取回
cuda.memcpy_dtoh_async(output_host, output_device, stream)

# 等待GPU上的任务完成
stream.synchronize()

# 对输出结果进行后处理
output_data = output_host.reshape(255, 13, 13)
output_data = np.transpose(output_data, [1, 2, 0])
anchors = np.array([[10, 14], [23, 27], [37, 58], [81, 82], [135, 169], [344, 319]])
BIASES = np.array([116, 90, 156, 198, 373, 326])

detection = []
for i in range(13):
    for j in range(13):
        for a in range(6):
            conf = 1 / (1 + np.exp(-output_data[i][j][a * 25 + 4]))
            if conf > 0.5:
                obj = 1 / (1 + np.exp(-output_data[i][j][a * 25 + 5]))
                x = (j + 0.5) * 32 + output_data[i][j][a * 25 + 0] * 32
                y = (i + 0.5) * 32 + output_data[i][j][a * 25 + 1] * 32
                w = np.exp(output_data[i][j][a * 25 + 2]) * anchors[a][0]
                h = np.exp(output_data[i][j][a * 25 + 3]) * anchors[a][1]
                x -= w / 2
                y -= h / 2
                x /= 416
                y /= 416
                w /= 416
                h /= 416
                classes = output_data[i][j][a * 25 + 6:]
                classes = np.exp(classes - np.max(classes)) / np.sum(np.exp(classes - np.max(classes)))
                classes = list(classes)
                detection.append((x, y, w, h, obj, conf, classes))

detection = sorted(detection, key=lambda x: x[5], reverse=True)

# 显示结果
im = cv2.imread('image.jpg')
for detect in detection:
    x, y, w, h = detect[:4]
    x *= im.shape[1]
    y *= im.shape[0]
    w *= im.shape[1]
    h *= im.shape[0]
    x -= w / 2
    y -= h / 2
    x, y, w, h = int(x), int(y), int(w), int(h)
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow('result', im)
cv2.waitKey(0)
cv2.destroyAllWindows()