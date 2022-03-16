import numpy as np
import publish
import time
import find_tube


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

        self.motor9 = motor()  # 右转
        self.motor10 = motor()  # 左转
        self.new_putdata = self.motor1.speed
        self.out_putdata = self.motor1.speed
        self.old_putdata = self.motor1.speed
        self.change = False
        self.speed_init()
        self.count = 0
        self.open_camera = True
        self.joy_node = False
        self.now_state = "move_on"
        self.old_state = "move_on"
        self.start = False
        self.turn_right_mode = False
        self.find_black = False
        self.photo_src = None
        self.dl_true = False
        self.state = -1
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
        if p == 1:
            self.out_putdata = self.motor3.speed
        if p == -1:
            self.out_putdata = self.motor4.speed
        if k == 1:
            self.out_putdata = self.motor1.speed
        if k == -1:
            self.out_putdata = self.motor2.speed
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
        self.motor7.speed = np.array([1525, 1850, 1850, 1520, 1500, 1500])
        self.motor8.speed = np.array([1150, 1500, 1500, 1150, 1500, 1500])
        self.motor9.speed = np.array([1525, 1700, 1725, 1520, 1500, 1500])
        self.motor10.speed = np.array([1300, 1500, 1500, 1300, 1500, 1500])

    def speed_update(self, center_error, angle_error, find_black, color, img_src):
        print("center_error" + str(center_error) + "\tangle_error" + str(angle_error) + "\n")
        if not self.turn_right_mode:
            self.zuni = False
            if angle_error < -0.2:  # right
                self.new_putdata = np.array(self.motor9.speed)
                self.now_state = "turn_right"
            if angle_error > 0.2:  # left
                self.new_putdata = np.array(self.motor10.speed)
                self.now_state = "turn_left"
            if center_error > 150:
                self.new_putdata = np.array(self.motor4.speed)
                self.now_state = "move_right"
            if center_error < -150:
                self.new_putdata = np.array(self.motor3.speed)
                self.now_state = "move_left"
            if angle_error < -0.40:  # right
                self.new_putdata = np.array(self.motor9.speed)
                self.now_state = "turn_right"
            if angle_error > 0.40:  # left
                self.new_putdata = np.array(self.motor10.speed)
                self.now_state = "turn_left"
            if center_error > 200:
                self.new_putdata = np.array(self.motor4.speed)
                self.now_state = "move_right"
            if center_error < -200:
                self.new_putdata = np.array(self.motor3.speed)
                self.now_state = "move_left"
            if center_error > 200 and angle_error < -0.40:
                self.new_putdata = np.array(self.motor7.speed)
                self.now_state = "move_right"
                self.turn_right_mode = True
            if -0.2 < angle_error < 0.2 and -80 < center_error < 80:
                self.new_putdata = np.array(self.motor1.speed)
                self.now_state = "move_on"
            if np.isnan(center_error):
                self.new_putdata = np.array(self.motor1.speed)
                self.now_state = "move_on"
        else:
            if self.turn_right_mode:
                if angle_error < 0.2:
                    self.turn_right_mode = False
        if self.now_state == "move_on":
            pass

        self.old_state = self.now_state
        self.motor_pid()

        if find_black == True:
            # self.photo_src = img_src
            self.find_black = True
            self.state = color
        self.send(find_black, color)
        # if color is not None:
        #     if len(color) != 0:
        #         print("color:"+str(color))
        #         center_y = (color[1] + color[3]) / 2
        #         # if center_y < 450:
        #         #     find_black = False
        #         self.send(find_black, color[5])
        #     else:
        #         self.send(False, 0)
        # else:
        #     center_y = 0
        #     self.send(False, 0)
        if self.change:
            print("the change is valid")
            time.sleep(0.3)
            self.change = False

    def black_dl(self):
        print(self.state)
        if self.find_black and self.dl_true == False:
            color = find_tube.dl_detect(self.photo_src, 8, True, True, False)
            if color is not None:
                self.state = color[5]
                self.dl_true = True
                print("dl_true")
            else:
                self.state = -1
Motor = motor_all()
