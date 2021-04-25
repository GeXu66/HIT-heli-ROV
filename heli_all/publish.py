import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Joy
import motor as dj
from camera import Camera

light_state = 0


def callback(data):
    if data.buttons[3] == 1:
        dj.Motor.open_camera = True
        Camera.re_open()
    if data.buttons[4] == 1:
        dj.Motor.open_camera = False
        Camera.camera_release()
        dj.Motor.open_camera = False
    if dj.Motor.joy_node:
        if data.axes[7] != 0 or data.axes[6] != 0:
            dj.Motor.horizon_move(data.axes[7], -data.axes[6])
        if data.buttons[0] == 1:
            dj.Motor.up()
        if data.buttons[1] == 1:
            dj.Motor.down()
        if data.buttons[8] == 1:
            dj.Motor.turn_left()
        if data.buttons[9] == 1:
            dj.Motor.turn_right()
        if data.buttons[6] == 1:
            dj.Motor.joy_node = False
    else:
        if data.buttons[0] == 1:
            dj.Motor.joy_node = True


def ros_init():
    global pub
    global rate
    try:
        rospy.init_node('ros_heli', anonymous=True)
        pub = rospy.Publisher('speed', Float64MultiArray, queue_size=10)
        rospy.Subscriber('joy', Joy, callback)
        rate = rospy.Rate(10)  # 10hz
    except rospy.ROSInterruptException:
        pass


def speed_run(find_black, color):
    if not rospy.is_shutdown():
        # ros_str = "speed %s %s %s %s" % (str(dj.Motor.out_putdata), str(find_black), str(color),str(dj.Motor.state))
        # rospy.loginfo(ros_str)
        output = dj.Motor.out_putdata.tolist()
        print(dj.Motor.count)
        if find_black:
            dj.Motor.count += 1
            if 10 < dj.Motor.count:
                if dj.Motor.state == -1:
                    output.append(0)
                elif dj.Motor.state == 0:
                    output.append(1.0)
                else:
                    output.append(2.0)
                dj.Motor.count += 1
            else:
                dj.Motor.count += 1
                output.append(0)
        else:
            dj.Motor.count=0
            output.append(0)
        # if find_black:
        #     if color == -1:
        #         output.append(0)
        #     if color == 0:
        #         output.append(1.0)
        #     if color == 1:
        #         output.append(2.0)
        # else:
        #     output.append(0)
        print(output)
        data = Float64MultiArray(data=output)
        pub.publish(data)
        rate.sleep()
