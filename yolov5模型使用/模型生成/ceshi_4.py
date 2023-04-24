# _*_coding:utf-8_*_
# 作者     : 梧桐晨夏
# 创建时间 :2023/4/14  21:58
# 文件     :ceshi_4.py
# IDE      :PyCharm

import tflite

model_path = 'path/to/your_model.tflite'

# Load TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path=model_path)

# Allocate memory for tensor
interpreter.allocate_tensors()