#include "mbot_linux_serial.h"

using namespace std;
using namespace boost::asio;
//串口相关对象
boost::asio::io_service iosev;
boost::asio::serial_port sp(iosev, "/dev/ttyUSB2");
boost::system::error_code err;
/********************************************************
            串口发送接收相关常量、变量、共用体对象
********************************************************/
const unsigned char ender[2] = {0x0d, 0x0a};
const unsigned char header[2] = {0x55, 0xaa};

//发送左右轮速控制速度共用体
/*union sendData
{
	short d;
	unsigned char data[2];
}leftVelSet,rightVelSet;
*/
//ROS发送给STM32的ROV控制速度共用体
union sendData
{
	short d;
	unsigned char data[2];
}T_Speed1,T_Speed2,T_Speed3,T_Speed4,T_Speed5,T_Speed6;

//接收数据（左轮速、右轮速、角度）共用体（-32767 - +32768）
/*
union receiveData
{
	short d;
	unsigned char data[2];
}leftVelNow,rightVelNow,angleNow;
*/
//接收的ROV速度共用体（-32767 - +32768）
union receiveData
{
	float d;
	unsigned char data[4];
}N_Speed1,N_Speed2,N_Speed3,N_Speed4,N_Speed5,N_Speed6;
/********************************************************
函数功能：串口参数初始化
入口参数：无
出口参数：
********************************************************/
void serialInit()
{
    sp.set_option(serial_port::baud_rate(115200));
    sp.set_option(serial_port::flow_control(serial_port::flow_control::none));
    sp.set_option(serial_port::parity(serial_port::parity::none));
    sp.set_option(serial_port::stop_bits(serial_port::stop_bits::one));
    sp.set_option(serial_port::character_size(8));
}
/********************************************************
/********************************************************
函数功能：将对机器人的左右轮子控制速度，打包发送给下位机
入口参数：机器人线速度、角速度
出口参数：
********************************************************/
void writeROVSpeed(double Speed1, double Speed2,double Speed3, double Speed4,double Speed5, double Speed6,unsigned char ctrlFlag)
{
    unsigned char buf[20] = {0};//
    int i, length = 0;

    T_Speed1.d  = Speed1;//mm/s
    T_Speed2.d  = Speed2;
    T_Speed3.d  = Speed3;//mm/s
    T_Speed4.d  = Speed4;
    T_Speed5.d  = Speed5;//mm/s
    T_Speed6.d  = Speed6;
    // 设置消息头
    for(i = 0; i < 2; i++)
        buf[i] = header[i];             //buf[0]  buf[1]

    // 设置机器人左右轮速度
    length = 13;
    buf[2] = length;                    //buf[2]
    for(i = 0; i < 2; i++)
    {
        buf[i + 3]  = T_Speed1.data[i];  //buf[3] buf[4]
        buf[i + 5]  = T_Speed2.data[i]; //buf[5] buf[6]
        buf[i + 7]  = T_Speed3.data[i];  //buf[7] buf[8]
        buf[i + 9]  = T_Speed4.data[i]; //buf[9] buf[10]
        buf[i + 11] = T_Speed5.data[i];  //buf[11] buf[12]
        buf[i + 13] = T_Speed6.data[i]; //buf[13] buf[14]
    }
    // 预留控制指令
    buf[3 + length - 1] = ctrlFlag;       //buf[15]

    // 设置校验值、消息尾
    buf[3 + length] = getCrc8(buf, 3 + length);//buf[16]
    buf[3 + length + 1] = ender[0];     //buf[17]
    buf[3 + length + 2] = ender[1];     //buf[18]

    // 通过串口下发数据
    boost::asio::write(sp, boost::asio::buffer(buf));
}
/********************************************************
函数功能：将对机器人的左右轮子控制速度，打包发送给下位机
入口参数：机器人线速度、角速度
出口参数：
********************************************************/
/*
void writeSpeed(double Left_v, double Right_v,unsigned char ctrlFlag)
{
    unsigned char buf[20] = {0};//
    int i, length = 0;

    leftVelSet.d  = Left_v;//mm/s
    rightVelSet.d = Right_v;

    // 设置消息头
    for(i = 0; i < 2; i++)
        buf[i] = header[i];             //buf[0]  buf[1]

    // 设置机器人左右轮速度
    length = 5;
    buf[2] = length;                    //buf[2]
    for(i = 0; i < 2; i++)
    {
        buf[i + 3] = leftVelSet.data[i];  //buf[3] buf[4]
        buf[i + 5] = rightVelSet.data[i]; //buf[5] buf[6]
    }
    // 预留控制指令
    buf[3 + length - 1] = ctrlFlag;       //buf[7]

    // 设置校验值、消息尾
    buf[3 + length] = getCrc8(buf, 3 + length);//buf[8]
    buf[3 + length + 1] = ender[0];     //buf[9]
    buf[3 + length + 2] = ender[1];     //buf[10]

    // 通过串口下发数据
    boost::asio::write(sp, boost::asio::buffer(buf));
}
*/
/********************************************************
函数功能：从下位机读取数据
入口参数：机器人左轮轮速、右轮轮速、角度，预留控制位
出口参数：bool
********************************************************/
bool readROVSpeed(double &R_Speed1,double &R_Speed2,double &R_Speed3,double &R_Speed4,unsigned char &ctrlFlag)
{
    char i, length = 0;
    unsigned char checkSum;
    unsigned char buf[150]={0};
    //=========================================================
    //此段代码可以读数据的结尾，进而来进行读取数据的头部
    try
    {
        boost::asio::streambuf response;
        boost::asio::read_until(sp, response, "\r\n",err);
        copy(istream_iterator<unsigned char>(istream(&response)>>noskipws),
        istream_iterator<unsigned char>(),
        buf);
    }
    catch(boost::system::system_error &err)
    {
        ROS_INFO("read_until error");
    }
    //=========================================================

    // 检查信息头
    if (buf[0]!= header[0] || buf[1] != header[1])   //buf[0] buf[1]
    {
        ROS_ERROR("Received message header error!");
        return false;
    }
    // 数据长度
    length = buf[2];                                 //buf[2]

    // 检查信息校验值
    checkSum = getCrc8(buf, 3 + length);             //buf[10] 计算得出
    if (checkSum != buf[3 + length])                 //buf[10] 串口接收
    {
        ROS_ERROR("Received data check sum error!");
        return false;
    }

    // 读取速度值
    for(i = 0; i < 4; i++)
    {
        N_Speed1.data[i] = buf[i + 15];  //buf[3] buf[4]
        N_Speed2.data[i] = buf[i + 19];   //buf[5] buf[6]
        N_Speed3.data[i] = buf[i + 23]; //buf[7] buf[8]
        N_Speed4.data[i] = buf[i + 27];
    }

    // 读取控制标志位
    ctrlFlag = buf[31];
    R_Speed1  =N_Speed1.d;
    R_Speed2  =N_Speed2.d;
    R_Speed3  =N_Speed3.d;
    R_Speed4  =N_Speed4.d;
    return true;
}
/********************************************************
函数功能：从下位机读取数据
入口参数：机器人左轮轮速、右轮轮速、角度，预留控制位
出口参数：bool
********************************************************/
/*
bool readSpeed(double &Left_v,double &Right_v,double &Angle,unsigned char &ctrlFlag)
{
    char i, length = 0;
    unsigned char checkSum;
    unsigned char buf[150]={0};
    //=========================================================
    //此段代码可以读数据的结尾，进而来进行读取数据的头部
    try
    {
        boost::asio::streambuf response;
        boost::asio::read_until(sp, response, "\r\n",err);
        copy(istream_iterator<unsigned char>(istream(&response)>>noskipws),
        istream_iterator<unsigned char>(),
        buf);
    }
    catch(boost::system::system_error &err)
    {
        ROS_INFO("read_until error");
    }
    //=========================================================

    // 检查信息头
    if (buf[0]!= header[0] || buf[1] != header[1])   //buf[0] buf[1]
    {
        ROS_ERROR("Received message header error!");
        return false;
    }
    // 数据长度
    length = buf[2];                                 //buf[2]

    // 检查信息校验值
    checkSum = getCrc8(buf, 3 + length);             //buf[10] 计算得出
    if (checkSum != buf[3 + length])                 //buf[10] 串口接收
    {
        ROS_ERROR("Received data check sum error!");
        return false;
    }

    // 读取速度值
    for(i = 0; i < 2; i++)
    {
        leftVelNow.data[i]  = buf[i + 3]; //buf[3] buf[4]
        rightVelNow.data[i] = buf[i + 5]; //buf[5] buf[6]
        angleNow.data[i]    = buf[i + 7]; //buf[7] buf[8]
    }

    // 读取控制标志位
    ctrlFlag = buf[9];

    Left_v  =leftVelNow.d;
    Right_v =rightVelNow.d;
    Angle   =angleNow.d;

    return true;
}
*/
/********************************************************
函数功能：获得8位循环冗余校验值
入口参数：数组地址、长度
出口参数：校验值
********************************************************/
unsigned char getCrc8(unsigned char *ptr, unsigned short len)
{
    unsigned char crc;
    unsigned char i;
    crc = 0;
    while(len--)
    {
        crc ^= *ptr++;
        for(i = 0; i < 8; i++)
        {
            if(crc&0x01)
                crc=(crc>>1)^0x8C;
            else
                crc >>= 1;
        }
    }
    return crc;
}
