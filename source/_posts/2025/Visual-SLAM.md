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

## 硬件测试：intel realsense depth camera D435i

### wsl挂载usb设备
使用usb3.2连接电脑，要在wsl中使用usb设备请参考[微软的文档](https://learn.microsoft.com/zh-cn/windows/wsl/connect-usb)。

首先安装[USBIPD-WIN项目](https://github.com/dorssel/usbipd-win/releases)

在windows powershell中使用`usbipd list`查看usb设备列表，然后根据总线ID共享设备`usbipd bind --busid 4-4`
```
PS C:\Users\Triority> usbipd list
Connected:
BUSID  VID:PID    DEVICE                                                        STATE
1-2    1462:7d42  USB 输入设备                                                  Not shared
1-5    1ea7:0064  USB 输入设备                                                  Not shared
1-6    1a2c:9ef4  USB 输入设备                                                  Not shared
1-14   8087:0026  英特尔(R) 无线 Bluetooth(R)                                   Not shared
2-1    8086:0b3a  Intel(R) RealSense(TM) Depth Camera 435i Depth, Intel(R) ...  Not shared

Persisted:
GUID                                  DEVICE

```
接下来应该附加USB设备`usbipd attach --wsl --busid 2-1`，但是报错：
```
PS C:\Users\Triority> usbipd attach --wsl --busid 2-1
usbipd: info: Using WSL distribution 'Ubuntu-20.04' to attach; the device will be available in all WSL 2 distributions.
usbipd: info: Detected networking mode 'virtioproxy'.
usbipd: error: Networking mode 'virtioproxy' is not supported.
```
显然需要修改网络模式，这里改成`mirrored`，这个模式的作用在[微软的文档有介绍](https://learn.microsoft.com/en-us/windows/wsl/networking#mirrored-mode-networking)

也就是配置文件`.wslconfig`内容为
```
[wsl2]
networkingMode=mirrored
```
此时将wsl重启`wsl --shutdown`
```
PS C:\Users\Triority> usbipd attach --wsl --busid 2-1
usbipd: info: Using WSL distribution 'Ubuntu-20.04' to attach; the device will be available in all WSL 2 distributions.
usbipd: info: Detected networking mode 'mirrored'.
usbipd: info: Using IP address 127.0.0.1 to reach the host.
WSL usbip: error: Attach Request for 2-1 failed - Device busy (exported)
usbipd: warning: The device appears to be used by Windows; stop the software using the device, or bind the device using the '--force' option.
usbipd: error: Failed to attach device with busid '2-1'.
```
按照要求强制执行`usbipd bind --busid 2-1 --force`并重启电脑

此时重新`usbipd attach --wsl --busid 2-1`并在ubuntu中查看usb设备
```
triority@Triority-Desktop:~$ lsusb
Bus 002 Device 002: ID 8086:0b3a Intel Corp. Intel(R) RealSense(TM) Depth Camera 435i
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

### 开发环境
Intel D435i相关链接：
+ [商品页面](https://www.intelrealsense.com/depth-camera-d435i/)
+ [datasheet](https://www.intelrealsense.com/download/21345/?tmstv=1697035582)
+ [SDK](https://github.com/IntelRealSense/librealsense/releases)
+ [ros1使用](https://github.com/IntelRealSense/realsense-ros/tree/ros1-legacy)

