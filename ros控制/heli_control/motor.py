import numpy as np
from heli_control import publish
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
        self.motor7 = motor()  # 右转
        self.motor8 = motor()  # 左转
        self.new_putdata = self.motor1.speed
        self.out_putdata = self.motor1.speed
        self.old_putdata = self.motor1.speed
        self.change = False
        self.speed_init()
        self.count = 0
        self.zuni = True
        self.open_camera = True
        self.joy_node = True
        self.now_state = "move_on"
        self.old_state = "move_on"

    def motor_pid(self):
        self.out_putdata = self.new_putdata
        # self.out_putdata = (self.new_putdata - self.old_putdata) * (self.count / 4.0) + self.old_putdata

    def up(self):
        self.out_putdata = self.motor5.speed

        self.send(False, 0)

    def down(self):
        self.out_putdata = self.motor6.speed

        self.send(False, 0)

    def turn_right(self):
        self.out_putdata = self.motor7.speed

        self.send(False, 0)

    def turn_left(self):
        self.out_putdata = self.motor8.speed

        self.send(False, 0)

    def horizon_move(self, k, p):  # k前后分量 左右分量
        if k > 0:
            if p > 0:
                self.out_putdata = np.array(k * (self.motor1.speed - 1500) + p * (self.motor4.speed - 1500) + 1500)
            else:
                self.out_putdata = np.array(k * (self.motor1.speed - 1500) - p * (self.motor3.speed - 1500) + 1500)
        else:
            if p > 0:
                self.out_putdata = np.array(-k * (self.motor2.speed - 1500) + p * (self.motor4.speed - 1500) + 1500)
            else:
                self.out_putdata = np.array(-k * (self.motor2.speed - 1500) - p * (self.motor3.speed - 1500) + 1500)
        self.send(False, 0)

    def send(self, find_black, color):

        publish.speed_run(find_black, color)

    def speed_init(self):
        self.motor1.speed = np.array([1500, 1500, 1548, 1435, 1500, 1500])
        self.motor2.speed = np.array([1600, 1425, 1500, 1500, 1500, 1500])
        self.motor3.speed = np.array([1500, 1550, 1500, 1405, 1500, 1500])
        self.motor4.speed = np.array([1425, 1500, 1560, 1500, 1500, 1500])
        self.motor5.speed = np.array([1500, 1500, 1500, 1500, 1500, 1500])
        self.motor6.speed = np.array([1500, 1500, 1500, 1500, 1700, 1300])
        self.motor7.speed = np.array([1500, 1850, 1850, 1500, 1500, 1500])
        self.motor8.speed = np.array([1150, 1500, 1500, 1150, 1500, 1500])

    def speed_update(self, center_error, angle_error, find_black, color):
        print("center_error" + str(center_error) + "\tangle_error" + str(angle_error) + "\n")
        self.count += 1
        if self.count > 3:
            self.zuni = False
            self.count = 0
            if angle_error < -0.2:  # right
                self.new_putdata = np.array(self.motor7.speed)
                self.now_state = "turn_right"
            if angle_error > 0.2:  # left
                self.new_putdata = np.array(self.motor8.speed)
                self.now_state = "turn_left"
            if center_error > 80:
                self.new_putdata = np.array(self.motor4.speed)
                self.now_state = "move_right"
            if center_error < -80:
                self.new_putdata = np.array(self.motor3.speed)
                self.now_state = "move_left"
            if angle_error < -0.45:  # right
                self.new_putdata = np.array(self.motor7.speed)
                self.now_state = "turn_right"
            if angle_error > 0.45:  # left
                self.new_putdata = np.array(self.motor8.speed)
                self.now_state = "turn_left"
            if center_error > 200:
                self.new_putdata = np.array(self.motor4.speed)
                self.now_state = "move_right"
            if center_error < -200:
                self.new_putdata = np.array(self.motor3.speed)
                self.now_state = "move_left"
            if -0.2 < angle_error < 0.2 and -80 < center_error < 80:
                self.new_putdata = np.array(self.motor1.speed)
                self.now_state = "move_on"
            if np.isnan(center_error):
                self.new_putdata = np.array(self.motor1.speed)
                self.now_state = "move_on"
        else:
            self.zuni = True

        if self.now_state == "move_on":
            pass
            # if self.old_state == "turn_right":
            #     self.new_putdata = np.array(self.motor8.speed)
            #     self.change = True
            # if self.old_state == "turn_left":
            #     self.new_putdata = np.array(self.motor7.speed)
            #     self.change = True
            # if self.old_state == "move_right":
            #     self.new_putdata = np.array(self.motor3.speed)
            #     self.change = True
            # if self.old_state == "move_right":
            #     self.new_putdata = np.array(self.motor4.speed)
            #     self.change = True
        self.old_state =self.now_state
        self.motor_pid()
        self.send(find_black, color)
        if self.change:
            print("the change is valid")
            time.sleep(0.3)
            self.change=False

Motor = motor_all()
