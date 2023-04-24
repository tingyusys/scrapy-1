# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/3/29  13:44
# 文件     :ceshi.py
# IDE      :PyCharm



# 导入本地类


from utils.augmentations import letterbox
from utils.general import (non_max_suppression, scale_coords)
from models.experimental import attempt_load

import torch
import cv2
import numpy as np


# conf_thres = 0.5
# iou_thres = 0.45

conf_thres = 0.3
iou_thres = 0.25
color = (0, 255, 0)

# 权重文件名
# weights = 'cs16.pt'
weights = "pt_file/best.pt"



device = 'cuda' if torch.cuda.is_available() else 'cpu'
# 判断设备类型并仅使用一张GPU进行测试
half = device != 'cpu'
# 载入模型
model = attempt_load(weights, device=device)

# 获取名字
names = model.names

# 将模型的stride赋给stride变量 32
stride = max(int(model.stride.max()), 32)  # model stride
print(device)
model.float()

cap = cv2.VideoCapture(0)  # 0表示第一个可用的摄像头
# 读取示例图像
# img = cv2.imread('people.png')

# imgss = img

while True:
    ret, frame = cap.read()  # 读取一帧图像
    # 调用letterbox函数
    # padded_img, dw, dh = letterbox(img, stride=stride)[0]
    img = letterbox(frame, stride=stride)[0]
    # 函数将一个内存不连续存储的数组转换为内存连续存储的数组,使得运行速度更快
    img = np.ascontiguousarray(img)
    # 把数组转换成张量,且二者共享内存
    img = torch.from_numpy(img).to(device)

    img = img.float()

    # 压缩数据维度
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]
    # 对tensor进行转置
    img = img.permute(0, 3, 1, 2)

    pred = model(img, augment=False, visualize=False)[0]

    # NMS 非极大值抑制 即只输出概率最大的分类结果
    pred = non_max_suppression(pred, conf_thres, iou_thres)

    # print(pred)

    # 处理预测识别结果
    for i, det in enumerate(pred):  # per image
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
            # 框选出检测结果
            for *xyxy, conf, cls in reversed(det):
                # 取2位小数
                result = '{:.3f}'.format(conf.item())
                cls = int(cls)

                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 3)
                cv2.putText(frame, "{}:".format(names[cls])+""+str(result), (int(xyxy[0]), int(xyxy[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # 调用CV显示结果图
    # 调用CV显示结果图
    b, g, r = cv2.split(frame)
    image_1 = cv2.merge([r, g, b])

    cv2.imshow("display", np.array(image_1))
    cv2.waitKey(1)