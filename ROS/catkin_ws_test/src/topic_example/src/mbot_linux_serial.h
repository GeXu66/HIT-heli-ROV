#ifndef MBOT_LINUX_SERIAL_H
#define MBOT_LINUX_SERIAL_H

#include <ros/ros.h>
#include <ros/time.h>
#include <geometry_msgs/TransformStamped.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <boost/asio.hpp>
#include <geometry_msgs/Twist.h>

void serialInit();
void writeSpeed(double Left_v, double Right_v,unsigned char ctrlFlag);
extern bool readSpeed(double &Left_v,double &Right_v,double &Angle,unsigned char &ctrlFlag);
void writeROVSpeed(double Speed1, double Speed2,double Speed3, double Speed4,double Speed5, double Speed6,unsigned char ctrlFlag);
extern bool readROVSpeed(double &R_Speed1,double &R_Speed2,double &R_Speed3,double &R_Speed4,unsigned char &ctrlFlag);
unsigned char getCrc8(unsigned char *ptr, unsigned short len);

#endif
