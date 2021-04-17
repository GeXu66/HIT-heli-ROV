cmake_minimum_required(VERSION 2.8.3)
project(topic_example)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  std_msgs
)


catkin_package(
  INCLUDE_DIRS include
#  LIBRARIES topic_example
#  CATKIN_DEPENDS roscpp std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)



add_executable(publish_node src/mbot_linux_serial.h
 src/mbot_linux_serial.cpp  src/publish_node.cpp)
target_link_libraries(publish_node ${catkin_LIBRARIES})

