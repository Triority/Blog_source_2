---
title: 本科毕业设计论文：巷道移动机器人SLAM技术研究
cover: /img/
date: 2025-02-6 20:41:20
categories: 
- [文档&笔记]
tags:
- ROS
---
# 计划完成的任务目标
+ 制作一台移动机器人
+ 使用三维激光雷达和毫米波雷达进行建图
+ 使用深度相机和imu数据融合进行建图和导航

# 三维激光雷达建图（LeGO-LOAM）
+ 算法：[LeGO-LOAM](https://github.com/RobustFieldAutonomyLab/LeGO-LOAM)
+ 激光雷达：[RS-Helios-5515](RS-Helios-5515产品手册.pdf)

## 通讯连接和基本配置
首先用交换机连接激光雷达和电脑，为了方便我决定在vmware中开发，系统为`Ubuntu 18.04`安装了`ROS1-melodic`。网络设置为桥接模式，系统内设置网络手动ip`192.168.1.102`，子网掩码`255.255.255.0`（雷达默认ip`192.168.1.200`发送udp数据包到`192.168.1.102`的端口`6699``7788`）

新建ros工作空间后`src`文件夹放入[雷达ros驱动](5515_SDK.rar)和[雷达话题定义(驱动文档也有说明)](rslidar_msg-master.zip)，按照里面的要求进行配置修改即可，以及`LeGO-LOAM`代码包，除了按照文档说明进行修改以外，还要将`CMakeLists.txt`第四行的c++版本14:`set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -O3")`。

设置雷达数据为我们使用的32线雷达，修改`LeGO-LOAM/include/utility.h`，这里我补充一些注释
```
// Mine
// 传感器垂直方向上的扫描线数量
extern const int N_SCAN = 32;
// 水平方向上扫描一周360度所采集的点数
extern const int Horizon_SCAN = 1800;
// 水平方向上的角度分辨率
extern const float ang_res_x = 0.2;
// 垂直方向上的角度分辨率（某些垂直角度分辨率可能不是均匀的，可以写平均值）
extern const float ang_res_y = 2.2;
// 最底部扫描线的垂直角度
extern const float ang_bottom = 55.0;
// 地面点分割或移除算法中，指定了一个扫描线的索引号。索引号小于或等于groundScanInd的扫描线上的点，会被认为是潜在的地面点
extern const int groundScanInd = 7;
```

由于雷达数据的格式不同，使用[rs_to_velodyne](https://github.com/HViktorTsoi/rs_to_velodyne)进行格式转化，`A ros tool for converting Robosense pointcloud to Velodyne pointcloud format, which can be directly used for downstream algorithm, such as LOAM, LEGO-LOAM, LIO-SAM, etc.`
使用`rostopic list`可以看到代码接收雷达topic`/rslidar_points`转换后发送到`/velodyne_points`
```
triority@ubuntu:~/Desktop/lidar$ rostopic list
/rosout
/rosout_agg
/rslidar_points
/velodyne_points
```

这里我由于openGL驱动问题导致rviz报错闪退，即使不闪退也不显示任何点云，要将其改为软件驱动。由于rviz错误log为空文件导致我很久没有找到问题所在。没有在物理机上试过不知道和vmware有没有关系
```
export LIBGL_ALWAYS_SOFTWARE=1
```

按照LeGO-LOAM文档要求在实际运行和使用rosbag时需要使用不同的roslaunch配置，具体是修改`LeGO-LOAM/launch/run.launch`的第四行，仿真下设置为false否则为true
```
<param name="/use_sim_time" value="false" />
```

由于雷达驱动和LeGO-LOAM都会启动rviz，我这里直接修改雷达驱动启动文件`rslidar_sdk-dev_opt/launch/start.launch`注释掉rviz的启动内容
```
<launch>
  <node pkg="rslidar_sdk" name="rslidar_sdk_node" type="rslidar_sdk_node" output="screen">
    <param name="config_path" value=""/>
  </node>
  <!-- rviz -->
  <!--<node pkg="rviz" name="rviz" type="rviz" args="-d $(find rslidar_sdk)/rviz/rviz.rviz" />-->
</launch>
```

## 建图测试
习惯上我喜欢先单独启动roscore
```
roscore
```

启动雷达：
```
roslaunch rslidar_sdk start.launch
```

启动雷达数据转换：
```
rosrun rs_to_velodyne rs_to_velodyne XYZIRT XIRI
```

启动建图：
```
roslaunch lego_loam run.launch
```

这时就可以使用激光雷达的数据进行建图了，下图是我所在的实验室
![](69a805494e5c171e8fcc88a78ff7393.png)

## 地图保存和数据记录
如果需要保存建好的地图，在建图快要结束时，打开终端订阅全局点云地图的话题`/laser_cloud_surround`保存为bag包，然后转bag为pcd，使用
`pcl_viewer`打开点云地图
```
triority@ubuntu:~/Desktop/lidar$ rosbag record /laser_cloud_surround
[ INFO] [1744615722.083300899]: Subscribing to /laser_cloud_surround
[ INFO] [1744615722.089056296]: Recording to '2025-04-14-00-28-42.bag'.

triority@ubuntu:~/Desktop/lidar$ rosrun pcl_ros bag_to_pcd 2025-04-14-00-28-42.bag /laser_cloud_surround pcd1
Creating directory pcd1
Saving recorded sensor_msgs::PointCloud2 messages on topic /laser_cloud_surround to pcd1
Got 1681 data points in frame /camera_init on topic /laser_cloud_surround with the following fields: x y z intensity
Data saved to pcd1/1744615726.458191872.pcd

triority@ubuntu:~/Desktop/lidar$ pcl_viewer pcd1/1744615726.458191872.pcd
```

此外也可以直接记录雷达原始数据，便于后续对算法进行改进测试比较等


# 使用wsl环境开发深度相机（已弃用）
{% note danger modern %}
此部分内容已经弃用，不打算使用深度相机了，但该过程未来仍有可能有参考价值，故保留。以及在wsl环境下即使挂载了usb设备，intel驱动程序也会报错检测不到深度相机，这一问题还没有解决。
{% endnote %}

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


**wsl挂载usb设备：**

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

Intel D435i相关链接：
+ [商品页面](https://www.intelrealsense.com/depth-camera-d435i/)
+ [datasheet](https://www.intelrealsense.com/download/21345/?tmstv=1697035582)
+ [SDK](https://github.com/IntelRealSense/librealsense/releases)
+ [ros1使用](https://github.com/IntelRealSense/realsense-ros/tree/ros1-legacy)

