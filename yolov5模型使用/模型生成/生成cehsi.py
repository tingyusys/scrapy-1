# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  17:36
# 文件     :生成cehsi.py
# IDE      :PyCharm

import torch
from models.experimental import attempt_load


# import tensorrt as trt


# 加载YOLOv3-Tiny模型
model = attempt_load('工件.pt', device="cpu")

# python export.py --weights best.pt --img 640 --batch 1

print(model)
# 置为评估模式
# model.eval()

# 剪枝模型
# pruned_model = torch.nn.Sequential(
#     # 原始模型层
#     model.modules()[:5],
#     # 剪枝下采样层
#     torch.nn.Conv2d(16, 32, 3, 2, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(32, 64, 3, 2, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(64, 128, 3, 2, 1),
#     torch.nn.ReLU(),
#     # 原始模型层
#     model.modules()[12:-1],
#     # 剪枝卷积层
#     torch.nn.Conv2d(128, 64, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(64, 128, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(128, 64, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(64, 128, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(128, 256, 3, 2, 1),
#     torch.nn.ReLU(),
#     # 原始模型层
#     model.modules()[-8:-3],
#     # 剪枝卷积层
#     torch.nn.Conv2d(256, 128, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(128, 256, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(256, 128, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(128, 256, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(256, 512, 3, 2, 1),
#     torch.nn.ReLU(),
#     # 原始模型层
#     model.modules()[-3:-1],
#     # 剪枝卷积层
#     torch.nn.Conv2d(512, 256, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(256, 512, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(512, 256, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(256, 512, 3, 1, 1),
#     torch.nn.ReLU(),
#     torch.nn.Conv2d(512, 255, 1, 1),
# )

# 导出模型为ONNX格式
dummy_input = torch.randn((1, 3, 416, 416))
input_names = ['input']
output_names = ['output']
# input_shapes = [(3, 416, 416)]

input_shape = (1, 3, 640, 640)
torch.onnx.export(model, torch.randn(input_shape), "yolov5s_pruned.onnx", opset_version=11)
# torch.onnx.export(model, dummy_input, 'yolov3-tiny.onnx',
#                   verbose=True, input_names=input_names, output_names=output_names,
#                   opset_version=10, input_shapes=input_shapes)

# 转换为TensorRT的引擎
# TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
# EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
# builder = trt.Builder(TRT_LOGGER)
# network = builder.create_network(EXPLICIT_BATCH)
# parser = trt.OnnxParser(network, TRT_LOGGER)

# with open('yolov3-tiny.onnx', 'rb') as model_file:
#     onnx_model = model_file.read()

# if not parser.parse(onnx_model):
#     print('ERROR: Failed to parse ONNX file!')
#     for error in range(parser.num_errors):
#         print(parser.get_error(error))
#     exit()

# builder.max_batch_size = 1
# builder.max_workspace_size = 1 << 30
# engine = builder.build_cuda_engine(network)

# 保存TensorRT引擎
# with open('yolov3-tiny.engine', 'wb') as engine_file:
#     engine_file.write(engine.serialize())