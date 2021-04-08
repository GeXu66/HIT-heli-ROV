# coding:utf-8
# Python中声明文件编码的注释，编码格式指定为utf-
# edit by LEZHI ROBOT SSS-LIUsq
# import RPi.GPIO as GPIO  # 引入块
import torch
import cv2  # 引入块
import numpy as np
from detect import detect

print("....ROBOTS START!!!...")  # 打印启动提示
global Path_Dect_px1  # 定义全局变量
Path_Dect_px1 = 320  # 赋值全局变量初值
global Path_Dect_px2  # 定义全局变量
Path_Dect_px2 = 320  # 赋值全局变量初值
global Path_Dect_px3  # 定义全局变量
Path_Dect_px3 = 320  # 赋值全局变量初值
global Path_Dect_px4  # 定义全局变量
Path_Dect_px4 = 320  # 赋值全局变量初值
global Path_Dect_pxcun1  # 定义全局变量，用来存储计算误差，程序中用于滤除干扰
Path_Dect_pxcun1 = 0  # 赋值全局变量初值
global Path_Dect_pxcun2  # 定义全局变量，用来存储计算误差，程序中用于滤除干扰
Path_Dect_pxcun2 = 0  # 赋值全局变量初值
global Path_Dect_pxcun3  # 定义全局变量，用来存储计算误差，程序中用于滤除干扰
Path_Dect_pxcun3 = 0  # 赋值全局变量初值
timet = 0  # 设置变量初始值为0
jishuT = 0  # 设置变量初始值为0
jishuT2 = 0  # 设置变量初始值为0
jishuT3 = 0  # 设置变量初始值为0
jiaodu = 0  # 设置变量初始值为0
ld = 0  # 设置变量初始值为0
ld1 = 0  # 设置变量初始值为0
ld2 = 0  # 设置变量初始值为0
ld3 = 0  # 设置变量初始值为0
ld4 = 0  # 设置变量初始值为0
one = 90  # 设置变量初始值为80
two = 80  # 设置变量初始值为70
three = 70  # 设置变量初始值为60
four = 50  # 设置变量初始值为50
mind = 60  # 设置变量初始值为
yx = 60  # 设置变量初始值为
yz = 200  # 设置变量初始值为
line1 = 160  # 设置变量初始值为
line2 = 320  # 设置变量初始值为
line3 = 480  # 设置变量初始值为
zuo1 = 80  # 设置边界变量初始值为
zuo2 = 140  # 设置边界变量初始值为
zuo3 = 200  # 设置边界变量初始值为
zuo4 = 260  # 设置边界变量初始值为
you1 = 360  # 设置边界变量初始值为
you2 = 420  # 设置边界变量初始值为
you3 = 480  # 设置边界变量初始值为
you4 = 540  # 设置边界变量初始值为


##########机器人方向控制###############
def Motor_Forward():  # 机器人前进子函数
    print('motor_Forward')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"G")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_Backward():  # 机器人运行子函数
    print('motor_backward')  # 机器人前进shell窗口打印字符用于提示程序运行状态


def Motor_TurnLeft():  # 机器人运行子函数
    print('motor_turnleft')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"F")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnLeft1():  # 机器人运行子函数
    print('motor_turnleft1')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"D")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnLeft2():  # 机器人运行子函数
    print('motor_turnleft2')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"S")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnLeft3():  # 机器人运行子函数
    print('motor_turnleft3')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"A")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnRight():  # 机器人运行子函数
    print('motor_turnright')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"H")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnRight1():  # 机器人运行子函数
    print('motor_turnright1')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"J")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnRight2():  # 机器人运行子函数
    print('motor_turnright2')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"K")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_TurnRight3():  # 机器人运行子函数
    print('motor_turnright3')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"L")  # 串口发送数据，主要是给下位机主控仓发送控制指令


def Motor_Stop():  # 机器人运行子函数
    print('motor_stop')  # 机器人前进shell窗口打印字符用于提示程序运行状态
    # ser.write(b"T")  # 串口发送数据，主要是给下位机主控仓发送控制指令


##########机器人相对方向控制###############
def jiance2():  # 屏幕横向640个像素点，中间值为320
    if (Path_Dect_px4 < int(zuo4)) & (Path_Dect_px4 > int(zuo3)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnLeft()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 <= int(zuo3)) & (Path_Dect_px4 > int(zuo2)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnLeft1()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 <= int(zuo2)) & (Path_Dect_px4 > int(zuo1)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnLeft2()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 <= int(zuo1)) & (Path_Dect_px4 >= 0):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnLeft3()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 > int(you1)) & (Path_Dect_px4 <= int(you2)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnRight()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 > int(you2)) & (Path_Dect_px4 <= int(you3)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnRight1()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 > int(you3)) & (Path_Dect_px4 <= int(you4)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnRight2()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 > int(you4)) & (Path_Dect_px4 <= 640):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_TurnRight3()  # 调用子函数，执行控制程序
    if (Path_Dect_px4 >= int(zuo4)) & (Path_Dect_px4 <= int(you1)):  # 判断图像处理后计算出来的点位与屏幕中像素点位置关系，同时执行校正。
        Motor_Forward()  # 调用子函数，执行控制程序


##########机器人测试数据显示###############
def xianshi_shuju():
    # print ('ld %d '%ld)   #打印巡线中心点坐标值
    # print ('ld1 %d '%ld1)   #打印巡线中心点坐标值
    # print ('ld2% d '%ld2)   #打印巡线中心点坐标值
    # print ('ld3 %d '%ld3)   #打印巡线中心点坐标值
    # print ('ld4 %d '%ld4)   #打印巡线中心点坐标值
    # print ('_h% d '%_h)   #打印巡线中心点坐标值
    # print (' 点1数求和 %d '%Path_Dect_fre_count)   #打印巡线中心点坐标值
    # print (' 点2数求和 %d '%Path_Dect_fre_count1)   #打印巡线中心点坐标值
    print(' 中心点1 %d ' % Path_Dect_px4)  # 在shell窗口打印Path_Dect_px数据
    '''print("yx",yx)#shell窗口打印变量
    print("yz",yz)#shell窗口打印变量
    print("one",one)#shell窗口打印变量
    print("two",two)#shell窗口打印变量
    print("three",three)#shell窗口打印变量
    print("four",four)#shell窗口打印变量
    print("mind",mind)#shell窗口打印变量
    print("line1",line1)#shell窗口打印变量
    print("line2",line2)#shell窗口打印变量
    print("line3",line3)#shell窗口打印变量
    print("jiaodu",jiaodu)#shell窗口打印变量'''
    cv2.circle(frame, (int(Path_Dect_px), int(line1)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px + 50), int(line1)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px - 50), int(line1)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px + 30), int(line1)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px - 30), int(line1)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px1), int(line2)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px2), int(line3)), 10, (255, 0, 255), 2)  # 在原始图像中画出圆点位置
    cv2.circle(frame, (int(Path_Dect_px3), int(line1)), 10, (255, 255, 0), 2)  # 在原始图像中画出圆点位置

    cv2.line(frame, (int(Path_Dect_px), int(line1)), (int(Path_Dect_px1), int(line2)), (0, 0, 255), 3);  # 在原始图像中画线
    cv2.line(frame, (int(Path_Dect_px1), int(line2)), (int(Path_Dect_px2), int(line3)), (0, 0, 255), 3);  # 在原始图像中画线
    cv2.line(frame, (int(Path_Dect_px), int(line1)), (int(Path_Dect_px2), int(line3)), (0, 0, 255), 3);  # 在原始图像中画线

    cv2.line(frame, (int(zuo4), 0), (int(zuo4), 480), (0, 255, 0), 1);  # 在原始图像中画线
    cv2.putText(frame, str(zuo4), (int(zuo4), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(zuo3), 0), (int(zuo3), 480), (0, 255, 0), 1);  # 在原始图像中画线
    cv2.putText(frame, str(zuo3), (int(zuo3), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(zuo2), 0), (int(zuo2), 480), (0, 0, 255), 1);  # 在原始图像中画线
    cv2.putText(frame, str(zuo2), (int(zuo2), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(zuo1), 0), (int(zuo1), 480), (0, 0, 255), 1);  # 在原始图像中画线
    cv2.putText(frame, str(zuo1), (int(zuo1), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符

    cv2.putText(frame, "1max", (540, 420), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))  # 打印字符
    cv2.putText(frame, "2max", (540, 400), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))  # 打印字符
    cv2.putText(frame, "3max", (540, 380), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))  # 打印字符
    cv2.putText(frame, "4max", (540, 360), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))  # 打印字符
    cv2.putText(frame, "||max", (540, 440), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))  # 打印字符

    cv2.putText(frame, str(one), (600, 420), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(two), (600, 400), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(three), (600, 380), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(four), (600, 360), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(mind), (600, 440), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符

    cv2.line(frame, (int(you4), 0), (int(you4), 480), (0, 0, 255), 1);  # 在原始图像中画线
    cv2.putText(frame, str(you4), (int(you4), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(you3), 0), (int(you3), 480), (0, 0, 255), 1);  # 在原始图像中画线
    cv2.putText(frame, str(you3), (int(you3), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(you2), 0), (int(you2), 480), (0, 255, 0), 1);  # 在原始图像中画线
    cv2.putText(frame, str(you2), (int(you2), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符
    cv2.line(frame, (int(you1), 0), (int(you1), 480), (0, 255, 0), 1);  # 在原始图像中画线
    cv2.putText(frame, str(you1), (int(you1), 480), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))  # 打印字符

    cv2.putText(frame, str(Path_Dect_px2), (int(Path_Dect_px2), int(line3)), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(Path_Dect_px1), (int(Path_Dect_px1), int(line2)), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 0, 255))  # 打印字符
    cv2.putText(frame, str(Path_Dect_px), (int(Path_Dect_px), int(line1)), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 0, 255))  # 打印字符
    cv2.namedWindow('erzhihua', 0)
    cv2.resizeWindow('erzhihua', 480, 480)
    cv2.moveWindow('erzhihua', 100, 100)
    cv2.imshow('erzhihua', thresh1)  # 树莓派桌面显示二值化图像，比较占资源调试完成后注释掉即可
    cv2.namedWindow('xunguan', 0)
    cv2.resizeWindow('xunguan', 480, 480)
    cv2.moveWindow('xunguan', 590, 100)
    cv2.imshow('xunguan', frame)  # 树莓派桌面显示原图像，比较占资源调试完成后注释掉即可


##########图像处理主程序###############
thresh_val = 50
relevance = 0
cap = cv2.VideoCapture('under_test/test1.webm')  # 启动摄像头
# width = 640  # 设置采集的图像宽度为640像素点
# height = 640  # 设置采集的图像的高度为480像素点
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置采集的图像宽度为640像素点
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置采集的图像的高度为480像素点
while (cap.isOpened()):  # 无限循环执行
    ##########白色巡管主程序###############
    ret, img_src = cap.read()
    img_src = cv2.resize(img_src, (640, 640))
    ret, img_1 = cv2.threshold(img_src[:, :, 1], 150, 255, cv2.THRESH_BINARY)
    ret, img_2 = cv2.threshold(img_src[:, :, 2], 150, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_and(img_1, img_2)
    track_img = np.where(img == 255)
    if (len(track_img[0]) == 0):
        print('Right!')
    else:
        # print(track_img)
        track_x = (track_img[0]).T
        track_y = (track_img[1]).T
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # fit linear function according to the white region
        pre_fit = np.polyfit(img.shape[1] - track_x + 1, track_y + 1, 1)  # #col = f(#row)
        pre_val = np.polyval(pre_fit, [0, img.shape[0] - 1]).astype(np.int)  # #col = f(#row)
        output_img = cv2.line(img, (int((pre_val[0] + pre_val[1]) / 2), img.shape[0]),
                              (int((pre_val[1] + pre_val[0]) / 2), 0), (0, 255, 0), 5)
        output_img = cv2.line(output_img, (pre_val[0], img.shape[0]), (pre_val[1], 0), (0, 0, 255),
                              5)  # point(#col(topmin butmax), # row)
        # calculate degree error
        pre_angle = (pre_val[0] - pre_val[1]) / np.sqrt((pre_val[0] - pre_val[1]) ** 2 + img.shape[0] ** 2)
        pre_angle = np.arcsin(pre_angle)
        output_img = cv2.putText(output_img, 'angle error:' + str(round(pre_angle, 7)),
                                 (int(img.shape[1] * 0.03), int(img.shape[0] * 0.1)),
                                 cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
        but_part = np.where(track_y > img.shape[0] - (img.shape[0] / 4))
        now_error = np.mean(track_x[but_part])
        now_error = now_error - img.shape[1] / 2
        output_img = cv2.putText(output_img, 'horizontal error:' + str(round(now_error, 7)),
                                 (int(img.shape[1] * 0.03), int(img.shape[0] * 0.2)),
                                 cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
        cv2.imshow('output', output_img)
        cv2.imshow('img', img_src)
        cv2.waitKey(30)
    ###########形状识别主程序###############
    print(torch.cuda.is_available())
    with torch.no_grad():
        show_img = detect(img_src, 'weights/best.pt', 640)
        print(show_img)
cv2.destroyAllWindows()
