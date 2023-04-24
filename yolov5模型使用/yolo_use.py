# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  11:38
# 文件     :yolo_use.py
# IDE      :PyCharm

import cv2
import numpy as np
import torch

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.augmentations import letterbox


class YOLOv5Detector:
    def __init__(self, weights_path, conf_thres=0.3, iou_thres=0.25, device='cuda'):
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

        self.device = device

        self.model = attempt_load(weights_path, device=self.device)
        if self.device == "cpu":
            self.model.float()
        else:
            self.model.float()

        self.names = self.model.names
        self.stride = max(int(self.model.stride.max()), 32)

    def detect(self, img):
        frame = img
        img = letterbox(img, stride=self.stride)[0]
        img = np.ascontiguousarray(img)
        if self.device == "cpu":
            img = torch.from_numpy(img).to(self.device).float() / 255.0
        else:
            img = torch.from_numpy(img).to(self.device).float() / 255.0
        if len(img.shape) == 3:
            img = img[None]
        img = img.permute(0, 3, 1, 2)
        pred = self.model(img, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)

        results = []
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    results.append({
                        "box": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
                        "conf": '{:.3f}'.format(float(conf)),
                        "class": self.names[int(cls)]
                    })

        return results


if __name__ == '__main__':
    yolo_use = YOLOv5Detector("pt_file/best.pt")

    cap = cv2.VideoCapture(0)  # 0表示第一个可用的摄像头
    color = (0, 255, 0)

    while True:
        ret, frame = cap.read()  # 读取一帧图像

        # [{'box': [178, 197, 231, 259], 'conf': 0.30560940504074097, 'class': 'stop'}]
        data_list = yolo_use.detect(frame)

        if data_list:
            cv2.rectangle(frame, (data_list[0]["box"][0], data_list[0]["box"][1]),
                          ((data_list[0]["box"][2], data_list[0]["box"][3])), color, 3)
            cv2.putText(frame, "{}:".format(data_list[0]["class"]) + "" + str(data_list[0]["conf"]),
                        (data_list[0]["box"][0], data_list[0]["box"][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 调用CV显示结果图
        b, g, r = cv2.split(frame)
        image_1 = cv2.merge([b, g, r])

        cv2.imshow("display", np.array(image_1))
        cv2.waitKey(1)
