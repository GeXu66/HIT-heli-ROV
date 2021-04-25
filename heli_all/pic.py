import threading
import motor
from tkinter import *
from tkinter import Tk
import mul_process

def update():
    i = 0
    for j in range(6):
        motor.Motor.motor1.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor1.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor2.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor2.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor3.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor3.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor4.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor4.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor5.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor5.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor6.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor6.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor7.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor7.speed[j]
        i += 1
    for j in range(6):
        motor.Motor.motor8.speed[j] = int(entry[i].get()) if entry[i].get() != '' else motor.Motor.motor8.speed[j]
        i += 1
    print("update success\n")
def pic_init():
    global entry
    entry = []
    string_var = []
    myWindow = Tk()
    # 设置标题
    myWindow.title('河狸冲冲冲')
    # 标签控件布局

    for i in range(6):
        string_var.append(StringVar())
        string_var[i].set(str(motor.Motor.out_putdata[i]))
        Label(myWindow, textvariable=string_var[i]).grid(row=i + 1, column=10)

    Label(myWindow, text="left before").grid(row=0, column=1)
    Label(myWindow, text="right before").grid(row=0, column=2)
    Label(myWindow, text="left behind").grid(row=0, column=3)
    Label(myWindow, text="right behind").grid(row=0, column=4)
    Label(myWindow, text="left up").grid(row=0, column=5)
    Label(myWindow, text="right up").grid(row=0, column=6)
    Label(myWindow, text="前进").grid(row=1)
    Label(myWindow, text="后退").grid(row=2)
    Label(myWindow, text="左平移").grid(row=3)
    Label(myWindow, text="右平移").grid(row=4)
    Label(myWindow, text="UP").grid(row=5)
    Label(myWindow, text="DOWN").grid(row=6)
    Label(myWindow, text="left转").grid(row=7)
    Label(myWindow, text="right转").grid(row=7)
    # Entry控件布局
    for i in range(8):
        for j in range(6):
            entry.append(Entry(myWindow))
            entry[i * 6 + j].grid(row=i + 1, column=j + 1)

    # Quit按钮退出；Run按钮打印计算结果
    Button(myWindow, text='Quit', command=myWindow.quit).grid(row=9, column=0, sticky=W, padx=5, pady=5)
    Button(myWindow, text='Update', command=update).grid(row=9, column=1, sticky=W, padx=5, pady=5)
    # 进入消息循环
    myWindow.mainloop()

class myThread_pic(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        # mul_process.threadLock.acquire()
        pic_init()
        # 释放锁，开启下一个线程
        # mul_process.threadLock.release()


def opentreaed():
    # 创建新线程
    thread3 = myThread_pic(3, "Thread-3", 3)
    # 开启新线程
    thread3.start()
