import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Joy
from heli_control import motor as dj
from test import joy_mode


def callback(data):
    if joy_mode:
        if data.axes[1] != 0 or data.axes[0] != 0:
            dj.Motor.horizon_move(data.axes[1], -data.axes[0])
        if data.buttons[0] == 1:
            dj.Motor.up()
        if data.buttons[1] == 1:
            dj.Motor.down()
        if data.buttons[9] == 1:
            dj.Motor.turn_left()
        if data.buttons[10] == 1:
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


def ros_run():
    if not rospy.is_shutdown():
        ros_str = "speed %s" % str(dj.Motor.out_putdata)
        rospy.loginfo(ros_str)
        data = Float64MultiArray(data=dj.Motor.out_putdata.tolist())
        pub.publish(data)
        rate.sleep()
