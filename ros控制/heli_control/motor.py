import numpy as np
from heli_control import ros
import time
class motor:
    def __init__(self):
        self.speed = np.zeros(6)
        for i in range(6):
            self.speed[i] = 1500

    def update(self, speed):
        self.speed = speed


class motor_all:
    def __init__(self):
        self.motor1 = motor()  # 前进
        self.motor2 = motor()  # 后退
        self.motor3 = motor()  # 左
        self.motor4 = motor()  # 右
        self.motor5 = motor()  # 上升
        self.motor6 = motor()  # 下潜
        self.motor7 = motor()  # 左转
        self.motor8 = motor()  # 右转
        self.new_putdata = self.motor1.speed
        self.out_putdata = self.motor1.speed
        self.old_putdata = self.motor1.speed
        self.change = False
        self.speed_init()
        self.count = 0
        self.zuni = True
    def motor_pid(self):
         # zuni
        if self.count>4:
            self.out_putdata = self.new_putdata
            self.old_putdata = self.out_putdata
        else:
            self.out_putdata = (self.new_putdata - self.old_putdata)*(self.count/4.0) + self.old_putdata
        self.change = True
        # time.sleep(0.02)
    def up(self):
        self.out_putdata = self.motor5.speed
        self.change = True

    def down(self):
        self.out_putdata = self.motor6.speed
        self.change = True

    def turn_right(self):
        self.out_putdata = self.motor7.speed
        self.change = True

    def turn_left(self):
        self.out_putdata = self.motor8.speed
        self.change = True

    def horizon_move(self, k, p):  # k前后分量 左右分量
        if k > 0:
            if p > 0:
                self.out_putdata = np.array(k * (self.motor1.speed - 1500) + p *(self.motor4.speed - 1500) +1500)
            else:
                self.out_putdata = np.array(k * (self.motor1.speed - 1500) + p * (self.motor3.speed - 1500)  +1500)
        else:
            if p > 0:
                self.out_putdata =np.array( k * (self.motor2.speed - 1500) + p * (self.motor4.speed - 1500) +1500)
            else:
                self.out_putdata =np.array( k * (self.motor2.speed - 1500) + p * (self.motor3.speed - 1500) +1500)
        self.change = True

    def send(self):
        self.change = False
        # test.srceen_update()
        ros.ros_run()

    def speed_init(self):
        self.motor1.speed = np.array([1500,1500,1550,1425,1500,1500])
        self.motor2.speed = np.array([1600,1425,1500,1500,1500,1500])
        self.motor3.speed = np.array([1500,1400,1500,1600,1500,1500])
        self.motor4.speed = np.array([1375,1500,1550,1500,1500,1500])
        self.motor5.speed = np.array([1500,1500,1500,1500,1500,1500])
        self.motor6.speed = np.array([1600,1425,1500,1500,1500,1500])
        self.motor7.speed = np.array([1500,1600,1600,1500,1500,1500])
        self.motor8.speed = np.array([1500,1375,1375,1500,1500,1500])

    def speed_update(self,center_error,angle_error):
        print("center_error"+str(center_error)+"\tangle_error"+str(angle_error)+"\n")
        self.count+=1
        if self.count>6:
            self.zuni  = False
            self.count= 0
            if center_error > 30:
                self.new_putdata =  np.array(0.5 * (self.motor4.speed - 1500)+1500)
                if center_error > 60:
                    self.new_putdata =  np.array(1 * (self.motor4.speed - 1500)+1500)
            if center_error < -30:
                self.new_putdata = np.array(0.5 * (self.motor3.speed - 1500)+1500)
                if center_error < -60:
                    self.new_putdata = np.array(1 * (self.motor3.speed - 1500) + 1500)
            if angle_error<-0.4:
                self.new_putdata = np.array(1 * (self.motor7.speed - 1500) + 1500)
            if angle_error>0.4:
                self.new_putdata = np.array(1 * (self.motor8.speed - 1500) + 1500)
            if -0.4<angle_error<0.4 and -30<center_error<30:
                self.new_putdata = np.array(1 * (self.motor1.speed - 1500) + 1500)
        else:
            self.zuni = True
        self.motor_pid()
        self.send()
Motor = motor_all()
