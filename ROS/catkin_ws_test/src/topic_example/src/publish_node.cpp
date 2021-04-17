
#include "ros/ros.h"
#include "std_msgs/Float64MultiArray.h" //use data struct of std_msgs/String
#include "mbot_linux_serial.h"

//test send value
double C_Speed1=1500.0;
double C_Speed2=1600.0;
double C_Speed3=1700.0;
double C_Speed4=1400.0;
double C_Speed5=1300.0;
double C_Speed6=1200.0;
int Direction = 1;
unsigned char C_Flag=0x07;

//test receive value
double row=0.0;
double yawl=0.0;
double pitch=0.0;
double depth=0.0;
double Read_Speed6=0.0;
unsigned char Read_Flag=0x00;

ros::Publisher chatter_pub;
void chatterCallback(const std_msgs::Float64MultiArray::ConstPtr& msg)
{
    C_Speed1 = msg->data.at(0);
    C_Speed2 = msg->data.at(1);
    C_Speed3 = msg->data.at(2);
    C_Speed4 = msg->data.at(3);
    C_Speed5 = msg->data.at(4);
    C_Speed6 = msg->data.at(5);
    writeROVSpeed((int)C_Speed1,(int)C_Speed2,(int)C_Speed3,(int)C_Speed4,(int)C_Speed5,(int)C_Speed6,C_Flag);
    ROS_INFO("write:%f,%f,%f,%f,%f,%f\n",C_Speed1,C_Speed2,C_Speed3,C_Speed4,C_Speed5,C_Speed6);
}

void timeCallback(const ros::TimerEvent& unuse)
{
    std_msgs::Float64MultiArray msg;
    readROVSpeed(depth,row,yawl,pitch,Read_Flag);
    ROS_INFO("%f,%f,%f,%f\n",depth,row,yawl,pitch);
    msg.data.push_back(row);
    msg.data.push_back(yawl);
    msg.data.push_back(pitch);
    msg.data.push_back(depth);
    chatter_pub.publish(msg);
}

int main(int agrc,char **argv)
{
    ros::init(agrc,argv,"public_node");
    ros::NodeHandle nh;
    ros::Timer timer = nh.createTimer(ros::Duration(0.05), timeCallback);
    ros::Rate loop_rate(10);
    ros::Subscriber sub = nh.subscribe("speed", 1000, chatterCallback);
    chatter_pub = nh.advertise<std_msgs::Float64MultiArray>("mcu", 1000);
    //串口初始化
    serialInit();
    ros::spin();
    return 0;
}




