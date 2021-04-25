import cv2
import numpy as np


def save_image(image, addr, num):
    address = addr + str(num) + '.jpg'
    cv2.imwrite(address, image)


# 读取视频文件
videoCapture = cv2.VideoCapture("new.mp4")
# 通过摄像头的方式
# videoCapture=cv2.VideoCapture(1)

# 读帧
success, frame = videoCapture.read()
i = 0
while success:
    i = i + 1
    save_image(frame, './square/', i)
    print('save image:', i)
    success, frame = videoCapture.read()
