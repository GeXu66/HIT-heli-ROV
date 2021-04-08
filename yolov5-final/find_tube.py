import cv2
import numpy as np
from rich import print
from detect import detect
import torch

# def detect_circle(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
#     circles1 = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, 1, 10, param1=100, param2=30, minRadius=10, maxRadius=40)
#     if circles1 != None:
#         circles = circles1[0, :, :]
#         circles = np.uint16(np.around(circles))
#         return circles
#     else:
#         pass

thresh_val = 50
cap = cv2.VideoCapture("under_test/test1.webm")
relevance = 0
line_center = 0
center_error = 0
top = 35
left = 35
width = 600
height = 600
while (cap.isOpened()):
    try:
        ret, img_src = cap.read()
        img_src = cv2.resize(img_src, (640, 640))
        ret, img_1 = cv2.threshold(img_src[:, :, 1], 150, 255, cv2.THRESH_BINARY)
        ret, img_2 = cv2.threshold(img_src[:, :, 2], 150, 255, cv2.THRESH_BINARY)
        img = cv2.bitwise_and(img_1, img_2)
        track_img = np.where(img == 255)
        if (len(track_img[0]) == 0):
            text = 'No Tube Find!Default Right!'
            print(text)
        else:
            print(track_img)
            track_x = (track_img[0]).T
            track_y = (track_img[1]).T
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            # fit linear function according to the white region
            pre_fit = np.polyfit(img.shape[1] - track_x + 1, track_y + 1, 1)  # #col = f(#row)
            pre_val = np.polyval(pre_fit, [0, img.shape[0] - 1]).astype(np.int)  # #col = f(#row)
            line_center = int((pre_val[0] + pre_val[1]) / 2)
            output_img = cv2.line(img, (line_center, img.shape[0]),
                                  (line_center, 0), (0, 255, 0), 5)
            output_img = cv2.line(output_img, (pre_val[0], img.shape[0]), (pre_val[1], 0), (0, 0, 255), 5)
            # calculate degree error
            pre_angle = (pre_val[0] - pre_val[1]) / np.sqrt((pre_val[0] - pre_val[1]) ** 2 + img.shape[0] ** 2)
            pre_angle = np.arcsin(pre_angle)
            output_img = cv2.putText(output_img, 'angle error:' + str(round(pre_angle, 7)),
                                     (int(img.shape[1] * 0.03), int(img.shape[0] * 0.1)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            but_part = np.where(track_y > img.shape[0] - (img.shape[0] / 4))
            now_error = np.mean(track_x[but_part])
            now_error = now_error - img.shape[1] / 2
            output_img = cv2.putText(output_img, 'horizontal error:' + str(round(now_error, 7)),
                                     (int(img.shape[1] * 0.03), int(img.shape[0] * 0.2)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            center_error = line_center - 320
            if (pre_angle < -0.1):
                text1 = 'Turn Right:' + str(pre_angle)
            elif (pre_angle > 0.1):
                text1 = 'Turn Left:' + str(pre_angle)
            else:
                text1 = 'Go forward:' + str(pre_angle)

            if (center_error < -10):
                text2 = 'Horizon Left:' + str(center_error)
            elif (center_error > 10):
                text2 = 'Horizon Right:' + str(center_error)
            else:
                text2 = 'Go forward:' + str(center_error)
            output_img = cv2.putText(output_img, text1, (int(img.shape[1] * 0.03), int(img.shape[0] * 0.3)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            output_img = cv2.putText(output_img, text2, (int(img.shape[1] * 0.03), int(img.shape[0] * 0.4)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.namedWindow('output', 0)
            cv2.moveWindow('output', 30, 10)
            cv2.imshow('output', output_img)
            cv2.namedWindow('img', 0)
            cv2.moveWindow('img', 650, 10)
            cv2.imshow('img', img_src)
            ###########形状识别主程序###############
            gray_img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
            gray_img = gray_img[int(top):(int(top) + int(height)), int(left):(int(left) + int(width))]
            ret, black_img = cv2.threshold(gray_img, 35, 255, cv2.THRESH_BINARY)
            black_cord = np.where(black_img == 0)
            # print(black_cord)
            if (len(black_cord[0]) > 5000):
                text3 = 'Find Black!'
            else:
                text3 = 'No Black!'
            black_img = cv2.cvtColor(black_img, cv2.COLOR_GRAY2BGR)
            black_img = cv2.putText(black_img, text3,
                                    (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.1)),
                                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            # if text3=='Find Black!':
            #     cv2.rectangle(black_img, (black_cord[0][0] - 10, black_cord[1][0] - 10),
            #                   (black_cord[0][-1] + 10, black_cord[1][-1] + 10), (0, 255, 0), 3)
            # else:
            #     pass
            cv2.imshow('find_black', black_img)
            cv2.moveWindow('find_black', 1300, 10)
            # circles = detect_circle(img_src)
            # print(circles)
            # print(torch.cuda.is_available())
            # with torch.no_grad():
            #     pred = detect(img_src, 'weights/best.pt', 640)
            # if (pred != None) and (len(pred[0].cpu().numpy()) != 0):
            #     """
            #         (x1, y1) = (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1]))
            #         (x2, y2) = (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3]))
            #         cupy_data = fromDlpack(to_dlpack(tensor_data))
            #     """
            #     print("==================================================================================")
            #     print(pred[0].cpu().numpy())
            #     show_img = img_src.transpose((1, 2, 0)).copy().astype(np.uint8)
            #     print(type(pred[0]))
            #     cv2.rectangle(show_img, (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1])),
            #                   (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3])), (0, 255, 0), 3)
            #     cv2.imshow('show', show_img)
            #     cv2.waitKey(10)
            # else:
            #     print('No object found!')
            cv2.waitKey(30)
    except:
        break
