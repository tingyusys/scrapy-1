# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  21:39
# 文件     :ceshi_3.py
# IDE      :PyCharm

import cv2
import numpy as np
import onnxruntime

def detect_objects(image, session):
    """
    使用 ONNX 模型检测输入图像中的目标。
    :param image: 检测的图像
    :param session: ONNX运行时的回话
    :return: 返回物体检测结果、置信度和类别信息。
    """
    # 调整图像尺寸
    resized = cv2.resize(image, (640, 640), interpolation=cv2.INTER_LINEAR)

    # 对图像进行预处理
    blob = cv2.dnn.blobFromImage(resized, 1 / 255.0, (640, 640), swapRB=True)

    # 运行 ONNX 模型获取输出
    outputs = session.run(None, {session.get_inputs()[0].name: blob})

    # 从输出中提取目标位置信息、置信度和类别信息
    detections = outputs[0][:, :, :4]
    confidences = outputs[0][:, :, 4]
    class_ids = outputs[0][:, :, 5]

    return detections, confidences, class_ids

def draw_detection(image, detections, confidences, class_ids):
    """
    在图像上绘制检测结果并显示。
    :param image: 检测的图像
    :param detections: 物体检测的结果
    :param confidences: 物体检测的置信度
    :param class_ids: 物体检测的类别信息
    :return:
    """
    # 获取检测结果数量
    num_detections = detections.shape[1]

    # 遍历所有检测结果
    for i in range(num_detections):
        # 获取目标位置信息和置信度
        xmin, ymin, xmax, ymax = detections[0, i, :]
        confidence = confidences[0, i]

        # 如果置信度足够高，就绘制边界框和标签
        if confidence > 0.4:
            # 获取类别信息
            class_id = int(class_ids[0, i])
            class_name = class_names[class_id]

            print((xmin, ymin), (xmax, ymax))
            # # 绘制边界框
            cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

            # 绘制类别标签
            label = "{}: {:.2f}%".format(class_name, confidence * 100)
            cv2.putText(image, label, (int(xmin), int(ymin) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 在窗口中显示图像
    cv2.imshow("Object Detection", image)

# 加载模型
session = onnxruntime.InferenceSession("best-sim.onnx")

# 获取类别信息
class_names = ["stop", "person", "bicycle", "car", "motorcycle",
               "airplane", "bus", "train", "truck", "boat", "traffic light",
               "fire hydrant", "stop sign", "parking meter", "bench", "bird",
               "cat", "dog", "horse", "sheep", "cow", "elephant", "bear",
               "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie",
               "suitcase", "frisbee", "skis", "snowboard", "sports ball",
               "kite", "baseball bat", "baseball glove", "skateboard",
               "surfboard", "tennis racket", "bottle", "wine glass", "cup",
               "fork", "knife", "spoon", "bowl", "banana", "apple",
               "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
               "donut", "cake", "chair", "couch", "potted plant", "bed",
               "dining table", "toilet", "tv", "laptop", "mouse", "remote",
               "keyboard", "cell phone", "microwave", "oven", "toaster",
               "sink", "refrigerator", "book", "clock", "vase", "scissors",
               "teddy bear", "hair drier", "toothbrush"]

cap = cv2.VideoCapture(0)
# 打开摄像头
# with cv2.VideoCapture(0) as cap:
    # 检测并显示图像
while True:
    # 读取当前帧
    ret, image = cap.read()

    # 检测物体
    detections, confidences, class_ids = detect_objects(image, session)

    # 在图像上绘制检测结果并显示
    draw_detection(image, detections, confidences, class_ids)

    # 按下 q 键退出程序
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源并关闭所有窗口
cv2.destroyAllWindows()

