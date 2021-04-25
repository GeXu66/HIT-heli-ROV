import publish
import mul_process
from find_tube import camera_control,dl_detect
from motor import Motor
from camera import Camera
# import pic
count = -1
DL = False
DEBUG = True
if __name__ == '__main__':
    publish.ros_init()
    mul_process.opentreaed()
    # pic.opentreaed()
    # picture = Camera.get_picture()
    # dl_detect(picture,0,True,True)
    while 1:
        if Camera.video.isOpened() and Motor.open_camera:
            count += 1
            picture = Camera.get_picture()
            center_error, angle_error, find_black, color = camera_control(picture, count, DEBUG, DL)
            Motor.speed_update(center_error, angle_error, find_black, color, picture)
        # if Motor.joy_node:
        #
        #     pass
        # else:
        #     if Camera.video.isOpened() and Motor.open_camera:
        #         count += 1
        #         picture = Camera.get_picture()
        #         center_error, angle_error, find_black, color = camera_control(picture, count, DEBUG, DL)
        #         Motor.speed_update(center_error, angle_error, find_black, color,picture)

