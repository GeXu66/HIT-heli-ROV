import camera
import ros
import mul_process
import pic
from find_tube import camera_control
from motor import Motor

count = -1
DL = True
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
        while video.video.isOpened():
            count += 1
            picture = video.get_picture()
            center_error, angle_error, find_black, color = camera_control(picture, count, DEBUG, DL)
            if find_black:
                Motor.speed_update(center_error, angle_error, find_black, color)
            else:
                Motor.speed_update(center_error, angle_error, find_black, color)
