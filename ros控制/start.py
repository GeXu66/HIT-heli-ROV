from heli_control import camera
from heli_control import publish
from heli_control import mul_process
from heli_control import pic
from heli_cv.yolov5_final.find_tube import camera_control
from heli_control.motor import Motor
from heli_control.camera import Camera
count = -1
DL = False
DEBUG = False
if __name__ == '__main__':
    publish.ros_init()
    mul_process.opentreaed()
    #pic.opentreaed()
    while 1:
        if Motor.joy_node:
            pass
        else:
            if Camera.video.isOpened() and Motor.open_camera:
                count += 1
                picture = Camera.get_picture()
                center_error, angle_error,find_black,color = camera_control(picture, count, DEBUG, DL)
                if find_black:
                    Motor.speed_update(center_error, angle_error,find_black,color)
                else:
                    Motor.speed_update(center_error, angle_error,find_black,color)
