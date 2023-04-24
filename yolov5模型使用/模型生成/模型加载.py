# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  18:16
# 文件     :模型加载.py
# IDE      :PyCharm
import numpy as np
import onnx
import cv2
import onnxruntime as ort


model = onnx.load("best.onnx")
ort_session = ort.InferenceSession("best.onnx")
cap = cv2.VideoCapture(0)  # 0表示第一个可用的摄像头
net = cv2.dnn.readNetFromONNX("best.onnx")

while True:
    ret, img = cap.read()
    if img.all():
        # 数据预处理
        # cv_std = (1, 0.229, 0.224, 0.225)
        # cv_mean = (255*0.485, 255*0.456, 255*0.406)
        # blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, mean=cv_mean)
        # cv2.divide(blob, cv_std, blob)
        #
        # # 模型推理
        # net.setInput(blob)
        out = net.forward()

        # 后处理
        predictions = np.argmax(out, axis=1)  # 获取预测结果

        # 解析输出
        pred_label = out.argmax()
        print("预测标签为：", pred_label)

        # 显示图像
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

