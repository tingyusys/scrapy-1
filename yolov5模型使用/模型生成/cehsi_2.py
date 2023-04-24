# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  20:43
# 文件     :cehsi_2.py
# IDE      :PyCharm


import cv2
import numpy as np
import onnxruntime

session = onnxruntime.InferenceSession("best.onnx")
cap = cv2.VideoCapture(0)  # 0表示第一个可用的摄像头
while True:
    ret, image = cap.read()

    resized = cv2.resize(image, (640, 640), interpolation=cv2.INTER_LINEAR)
    img_in = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    img_in = np.transpose(img_in, (2, 0, 1)).astype(np.float32)
    img_in = np.expand_dims(img_in, axis=0)
    img_in /= 255.0

    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img_in})


    # 获取物体检测结果
    detections = outputs[0][:, :, :4]  # (1, 25200, 4)；分别为xmin、ymin、xmax、ymax

    # 获取物体置信度
    confidences = outputs[0][:, :, 4]  # (1, 25200)

    # 获取类别信息
    class_ids = outputs[0][:, :, 5]  # (1, 25200)

    xmin = detections[0, :, 0]  # 所有目标的xmin
    ymin = detections[0, :, 1]  # 所有目标的ymin
    xmax = detections[0, :, 2]  # 所有目标的xmax
    ymax = detections[0, :, 3]  # 所有目标的ymax


    print(xmin[0])

    cv2.imshow("img", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





