---
title: 本科毕业设计论文：巷道移动机器人SLAM技术研究
cover: /img/
date: 2025-02-6 20:41:20
categories: 
- [文档&笔记]
tags:
- ROS
---
# 主要任务目标
+ 制作一台移动机器人
+ 使用深度相机和imu数据融合进行建图和导航

# 实现过程
## 实验环境
目前还在寒假期间没有实物制作的条件，打算先跑跑仿真，准备好技术路线。目前打算在windows系统中使用wsl2的ubuntu20进行开发

<details>
<summary>wsl内安装ros后无法启动roscore的问题</summary>
```
triority@Triority-Desktop:~$ roscore
... logging to /home/triority/.ros/log/499be312-e486-11ef-add2-75fb32d30971/roslaunch-Triority-Desktop-36755.log
Checking log directory for disk usage. This may take a while.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is 1GB.
```
启动之后卡死在这里。主要原因是虚拟机内网络问题。$ROS_MASTER_URI通常是http://localhost:11311，$ROS_IP通常是WSL的IP地址，这里没有显示，指定为本机IP后问题解决：
```
triority@Triority-Desktop:~$ echo $ROS_MASTER_URI
http://localhost:11311
triority@Triority-Desktop:~$ echo $ROS_IP

triority@Triority-Desktop:~$ export ROS_IP=192.168.0.100
triority@Triority-Desktop:~$ echo $ROS_IP
192.168.0.100

triority@Triority-Desktop:~$ roscore
... logging to /home/triority/.ros/log/f7cd5362-e486-11ef-add2-75fb32d30971/roslaunch-Triority-Desktop-36776.log
Checking log directory for disk usage. This may take a while.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is <1GB.

started roslaunch server http://192.168.0.100:42277/
ros_comm version 1.17.0


SUMMARY
========

PARAMETERS
 * /rosdistro: noetic
 * /rosversion: 1.17.0

NODES

auto-starting new master
process[master]: started with pid [36784]
ROS_MASTER_URI=http://192.168.0.100:11311/

setting /run_id to f7cd5362-e486-11ef-add2-75fb32d30971
process[rosout-1]: started with pid [36794]
started core service [/rosout]
^C[rosout-1] killing on exit
[master] killing on exit
shutting down processing monitor...
... shutting down processing monitor complete
done
```

</details>

创建ros的工作空间之后在src文件夹新建一个包用于试验代码：
```
catkin_create_pkg lab roscpp rospy std_msgs
```
