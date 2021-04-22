import cv2
import numpy as np
# from rich import print
from detect import detect
import torch


def deal_pic(src):
    img_src = cv2.resize(src, (640, 640))
    ret, img_1 = cv2.threshold(img_src[:, :, 1], 150, 255, cv2.THRESH_BINARY)
    ret, img_2 = cv2.threshold(img_src[:, :, 2], 150, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_and(img_1, img_2)
    track_img = np.where(img == 255)
    return img_src, track_img, img


def find_black(img_src, top=35, left=35, width=600, height=600):
    gray_img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    gray_img = gray_img[int(top):(int(top) + int(height)), int(left):(int(left) + int(width))]
    ret, black_img = cv2.threshold(gray_img, 35, 255, cv2.THRESH_BINARY)
    black_cord = np.where(black_img == 0)
    return gray_img, black_img, black_cord


def dl_detect(img_src, count, DL=False, dl_flag=False, DEBUG=False):
    if DL:
        if count == 0:
            print(torch.cuda.is_available())
            with torch.no_grad():
                detect(img_src, 'weights/best.pt', 640, device='gpu', DEBUG=DEBUG)
            count += 1
        else:
            pass
        if dl_flag:
            if count % 5 == 0:
                with torch.no_grad():
                    detect(img_src, 'weights/best.pt', 640, device='gpu', DEBUG=DEBUG)
                count += 1
            else:
                count += 1
        else:
            pass
    else:
        pass


def poly_fit(track_img, img, DEBUG):
    track_x = (track_img[0]).T
    track_y = (track_img[1]).T
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # fit linear function according to the white region
    pre_fit = np.polyfit(img.shape[1] - track_x + 1, track_y + 1, 1)  # #col = f(#row)
    pre_val = np.polyval(pre_fit, [0, img.shape[0] - 1]).astype(int)  # #col = f(#row)
    line_center = int((pre_val[0] + pre_val[1]) / 2)
    # calculate degree error
    pre_angle = (pre_val[0] - pre_val[1]) / np.sqrt((pre_val[0] - pre_val[1]) ** 2 + img.shape[0] ** 2)
    pre_angle = np.arcsin(pre_angle)
    but_part = np.where(track_y > img.shape[0] - (img.shape[0] / 4))
    if len(track_x[but_part]) == 0:
        now_error = 0
    else:
        now_error = np.mean(track_x[but_part])
    now_error = now_error - img.shape[1] / 2
    if DEBUG:
        output_img = cv2.line(img, (line_center, img.shape[0]),
                              (line_center, 0), (0, 255, 0), 5)
        output_img = cv2.line(output_img, (pre_val[0], img.shape[0]), (pre_val[1], 0), (255, 0, 0), 5)
        output_img = cv2.putText(output_img, 'angle error:' + str(round(pre_angle, 7)),
                                 (int(img.shape[1] * 0.03), int(img.shape[0] * 0.1)),
                                 cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        output_img = cv2.putText(output_img, 'horizontal error:' + str(round(now_error, 7)),
                                 (int(img.shape[1] * 0.03), int(img.shape[0] * 0.2)),
                                 cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    else:
        output_img = None
    return line_center, pre_angle, now_error, output_img


def judge_direction(horizon_error, pre_angle):
    if pre_angle < -0.1:
        text1 = 'Turn Right:' + str(pre_angle)
    elif pre_angle > 0.1:
        text1 = 'Turn Left:' + str(pre_angle)
    else:
        text1 = 'Go forward:' + str(pre_angle)

    if horizon_error < -10:
        text2 = 'Horizon Left:' + str(horizon_error)
    elif horizon_error > 10:
        text2 = 'Horizon Right:' + str(horizon_error)
    else:
        text2 = 'Go forward:' + str(horizon_error)
    return text1, text2


def camera_control(src, count, DEBUG, DL):
    if DEBUG:
        img_src, track_img, img = deal_pic(src)
        if len(track_img[0]) == 0:
            text = 'No Tube Find!Default Right!'
            print(text)
            return 0, -1.0, False, 0
        else:
            # print(track_img)
            line_center, pre_angle, now_error, output_img = poly_fit(track_img, img, DEBUG)
            center_error = line_center - int(img_src.shape[1] / 2)
            text1, text2 = judge_direction(center_error, pre_angle)
            output_img = cv2.putText(output_img, text1, (int(img.shape[1] * 0.03), int(img.shape[0] * 0.3)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            output_img = cv2.putText(output_img, text2, (int(img.shape[1] * 0.03), int(img.shape[0] * 0.4)),
                                     cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.namedWindow('output', 0)
            cv2.moveWindow('output', 30, 10)
            # print(output_img.shape())
            cv2.imshow('output', output_img)
            cv2.waitKey(1)
            cv2.namedWindow('img', 0)
            cv2.moveWindow('img', 650, 10)
            # print(img_src.shape())
            cv2.imshow('img', img_src)
            cv2.waitKey(1)
            gray_img, black_img, black_cord = find_black(img_src, top=35, left=35, width=600, height=600)
            # print(black_cord)
            if len(black_cord[0]) > 5000:
                text3 = 'Find Black!'
                dl_flag = True
            else:
                text3 = 'No Black!'
                dl_flag = False
            black_img = cv2.cvtColor(black_img, cv2.COLOR_GRAY2BGR)
            black_img = cv2.putText(black_img, text3,
                                    (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.1)),
                                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('find_black', black_img)
            cv2.moveWindow('find_black', 1300, 10)
            cv2.waitKey(1)
            dl_detect(img_src, count, DL, dl_flag, DEBUG)
            return center_error, pre_angle, False, 0
    else:
        img_src, track_img, img = deal_pic(src)
        if len(track_img[0]) == 0:
            print('No Tube Find!Default Right!')
            return 0, -1.0, False, 0
        else:
            # print(track_img)
            line_center, pre_angle, now_error, output_img = poly_fit(track_img, img, DEBUG)
            center_error = line_center - int(img_src.shape[1] / 2)
            gray_img, black_img, black_cord = find_black(img_src, top=35, left=35, width=600, height=600)
            # print(black_cord)
            if len(black_cord[0]) > 5000:
                text3 = 'Find Black!'
                dl_flag = True
                # color = dl_detect(img_src, count, DL, dl_flag, DEBUG)
                dl_detect(img_src, count, DL, dl_flag, DEBUG)
                return center_error, pre_angle, True, 1
            else:
                text3 = 'No Black!'
                dl_flag = False
            return center_error, pre_angle, False, 0


cap = cv2.VideoCapture("under_test/test1.webm")
count = -1
while cap.isOpened():
    count += 1
    ret, frame = cap.read()
    if frame is not None:
        camera_control(frame, count, DEBUG=True, DL=True)
    else:
        exit(0)
