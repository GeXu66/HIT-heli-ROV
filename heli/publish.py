import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Joy
import heli_control.motor as dj


def callback(data):
    if True:
        if data.axes[1] != 0 or data.axes[0] != 0:
            dj.Motor.horizon_move(data.axes[1], -data.axes[0])
        if data.buttons[0] == 1:
            dj.Motor.up()
        if data.buttons[1] == 1:
            dj.Motor.down()
        if data.buttons[8] == 1:
            dj.Motor.turn_left()
        if data.buttons[9] == 1:
            dj.Motor.turn_right()
    else:
        pass


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
        ros_str = "speed %s %s %s" % (str(dj.Motor.out_putdata), str(find_black), str(color))
        rospy.loginfo(ros_str)
        output = dj.Motor.out_putdata.tolist()
        if find_black:
            if color == 0:
                output.append(1.0)
            else:
                output.append(2.0)
        else:
            output.append(0)
        data = Float64MultiArray(data=output)
        pub.publish(data)
        rate.sleep()
    pass
