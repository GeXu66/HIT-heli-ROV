import cv2
import numpy as np
# from rich import print
from detect import detect
import torch

had_find = -1
now_state = False
last_state = False


def ls_find(black_cord, black_img):
    global had_find
    global now_state
    global last_state
    # ls = [-1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ls = [1,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    x = np.mean(black_cord[1])
    x = int(x)
    y = np.mean(black_cord[0])
    y = int(y)
    black_img = cv2.cvtColor(black_img, cv2.COLOR_GRAY2BGR)
    black_img = cv2.circle(black_img, (x, y), 1, (0, 0, 255), 4)
    if y > 3 * black_img.shape[0] / 4:
        result = 'True'
        now_state = True
        flag = True
        if last_state:
            pass
        else:
            had_find += 1
    else:
        result = 'False'
        flag = False
        now_state = False
    last_state = now_state
    black_img = cv2.putText(black_img, result,
                            (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.2)),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    if ls[had_find] == 0:
        black_img = cv2.putText(black_img, 'circle',
                                (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.3)),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    else:
        black_img = cv2.putText(black_img, 'square',
                                (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.4)),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    if ls[had_find] == -1:
        flag = False
    if flag:
        return black_img, flag, ls[had_find]
    else:
        return black_img, flag, 0


def deal_pic(src):
    top = 0
    left = 0
    width = 640
    height = 470
    img_src = cv2.resize(src, (640, 640))
    ret, img_1 = cv2.threshold(img_src[:, :, 1], 150, 255, cv2.THRESH_BINARY)
    ret, img_2 = cv2.threshold(img_src[:, :, 2], 150, 255, cv2.THRESH_BINARY)
    img_2 = img_2[int(top):(int(top) + int(height)), int(left):(int(left) + int(width))]
    # img = cv2.bitwise_and(img_1, img_2)
    track_img = np.where(img_2 == 255)
    return img_src, track_img, img_2


def find_black(img_src, top=35, left=35, width=600, height=500):
    gray_img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    gray_img = gray_img[int(top):(int(top) + int(height)), int(left):(int(left) + int(width))]
    ret, black_img = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY)
    black_cord = np.where(black_img == 0)
    return gray_img, black_img, black_cord


def dl_detect(img_src, count, DL=False, dl_flag=False, DEBUG=False):
    if DL:
        if count == 0:
            print(torch.cuda.is_available())
            with torch.no_grad():
                morph = detect(img_src, 'weights/final.pt', 640, device='cpu', DEBUG=DEBUG)
            count += 1
        else:
            pass
        if dl_flag:
            if count % 8 == 0:
                with torch.no_grad():
                    morph = detect(img_src, 'weights/final.pt', 640, device='cpu', DEBUG=DEBUG)
                count += 1
                return morph
            else:
                count += 1
        else:
            pass
    else:
        pass


def poly_fit(track_img, img, DEBUG):
    track_img0 = track_img[0]
    track_img1 = track_img[1]
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = img[int(0):int(640), int(0):int(640)]
    track_x = track_img0.T
    track_y = track_img1.T
    # fit linear function according to the white region
    pre_fit = np.polyfit(img.shape[1] - track_x + 1, track_y + 1, 1)  # #col = f(#row)
    pre_val = np.polyval(pre_fit, [0, img.shape[0] - 1]).astype(int)  # #col = f(#row)
    line_center = int((pre_val[0] + pre_val[1]) / 2)
    # calculate degree error
    pre_angle = (pre_val[0] - pre_val[1]) / np.sqrt((pre_val[0] - pre_val[1]) ** 2 + img.shape[0] ** 2)
    pre_angle = np.arcsin(pre_angle)
    but_part = np.where(track_y > img.shape[0] - (img.shape[0] / 3))
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
            center_error = line_center - int(img.shape[1] / 2)
            if center_error == -320:
                center_error = np.mean(track_img[0]) - int(img.shape[1] / 2)
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
            # cv2.namedWindow('img', 0)
            # cv2.moveWindow('img', 650, 10)
            # # print(img_src.shape())
            # cv2.imshow('img', img_src)
            cv2.waitKey(1)
            gray_img, black_img, black_cord = find_black(img_src, top=50, left=50, width=600, height=460)
            # print(black_cord)
            if 2500 < len(black_cord[0]):
                text3 = 'Find Black!'
                black_img, flag, morph = ls_find(black_cord, black_img)
            else:
                text3 = 'No Black!'
                flag = False
                morph = 0
            # black_img = cv2.cvtColor(black_img, cv2.COLOR_GRAY2BGR)
            black_img = cv2.putText(black_img, text3,
                                    (int(black_img.shape[1] * 0.03), int(black_img.shape[0] * 0.1)),
                                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('find_black', black_img)
            cv2.moveWindow('find_black', 400, 10)
            cv2.waitKey(1)
            # morph = dl_detect(img_src, count, DL, dl_flag, DEBUG)
            return int(center_error), pre_angle, flag, morph
    else:
        img_src, track_img, img = deal_pic(src)
        if len(track_img[0]) == 0:
            print('No Tube Find!Default Right!')
            return 0, -1.0, False, 0
        else:
            # print(track_img)
            line_center, pre_angle, now_error, output_img = poly_fit(track_img, img, DEBUG)
            center_error = line_center - int(img.shape[1] / 2)
            if center_error == -320:
                center_error = np.mean(track_img[0]) - int(img.shape[1] / 2)
            gray_img, black_img, black_cord = find_black(img_src, top=50, left=50, width=600, height=470)
            # print(black_cord)
            if 2500 < len(black_cord[0]):
                text3 = 'Find Black!'
                dl_flag = True
                black_img, flag, morph = ls_find(black_cord, black_img)
                # color = dl_detect(img_src, count, DL, dl_flag, DEBUG)
                # morph = dl_detect(img_src, count, DL, dl_flag, DEBUG)
                return center_error, pre_angle, flag, morph
            else:
                text3 = 'No Black!'
                dl_flag = False
                return center_error, pre_angle, False, 0


cap = cv2.VideoCapture("under_test/Webcam/2021-04-17-013257.webm")
count = -1
while cap.isOpened():
    count += 1
    ret, frame = cap.read()
    if frame is not None:
        camera_control(frame, count, DEBUG=True, DL=False)
    else:
        exit(0)
