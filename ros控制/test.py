from heli_control import camera
from heli_control import ros
from heli_control import mul_process
from heli_control import pic
from heli_cv.yolov5_final.find_tube import cameara_control
from heli_control.motor import Motor
import Jetson
DEBUG = False
joy_mode = False

if __name__ == '__main__':
    ros.ros_init()
    mul_process.opentreaed()
    # pic.opentreaed()

    if joy_mode:
        pass
    else:
        video = camera.camera()
        find_black = False
        while video.video.isOpened():
            picture = video.get_picture()
            centre_error,angle_error = cameara_control(picture)
            if find_black:
                pass
            else:
                Motor.speed_update(centre_error,angle_error)
