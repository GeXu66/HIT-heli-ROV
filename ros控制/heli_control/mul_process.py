import threading
from heli_control import motor
import rospy
threadLock = threading.Lock()


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        speed_get()
        # 释放锁，开启下一个线程
        threadLock.release()

class myThread_ros(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        rospy.spin()
        # 释放锁，开启下一个线程
        threadLock.release()


def opentreaed():
    threads = []

    # 创建新线程
    # thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread_ros(2,'Thread-2',2)
    # 开启新线程
    # thread1.start()
    thread2.start()
    # 添加线程到线程列表
    # threads.append(thread1)
    threads.append(thread2)


def speed_get():
    while 1:
        if motor.Motor.change:
            motor.Motor.send()


