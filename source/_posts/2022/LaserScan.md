---
title: 激光雷达数据结构及使用opencv的可视化
date: 2022-10-27 21:23:45
tags:
- python
- ROS
- 笔记
- opencv
description: 用于使用激光雷达识别目标
cover: /img/LaserScan.png
categories: 
- 折腾记录
---
## 激光雷达数据结构
```
rosmsg show sensor_msgs/LaserScan
```
可以看到ros输出的激光雷达数据结构：
```
std_msgs/Header header   # Header也是一个结构体,包含了seq,stamp,frame_id,其中seq
                         # 指的是扫描顺序增加的id,stamp包含了开始扫描的时间和与开始扫
                         # 描的时间差,frame_id是扫描的参考系名称.注意扫描是逆时针从正前方开始扫描的.   
　　uint32 seq
　　time stamp
　　string frame_id 　　  # frame在ROS中作用至关重要，消息将和tf绑定才可以读取数据，
float32 angle_min        # 开始扫描的角度(rad)
float32 angle_max        # 结束扫描的角度(rad)
float32 angle_increment  # 每一次扫描增加的角度(rad)

float32 time_increment   # 测量的时间间隔(second)
float32 scan_time        # 扫描的时间间隔(second)

float32 range_min        # 距离最小值(m)
float32 range_max        # 距离最大值(m)

float32[] ranges         # 距离数组(m) (长度360)
float32[] intensities    # 与设备有关,强度数组(长度360)
```
我们主要需要的就是其中的`angle_increment`，`ranges`。
下面的程序用于将激光雷达数据可视化，更便于理解使用：
```python
import rospy
import cv2
import numpy as np
import math
from sensor_msgs.msg import LaserScan

def callback(data):
    # 设置画布为600*600像素
    frame = np.zeros((600, 600,3), np.uint8)
    angle = data.angle_min
    cv2.circle(frame, (300,300), 35, (0,255,0), -1)
    print(len(data.ranges))
    for r in data.ranges:
        if math.isinf(r) == True:
            r = 1000
        #这里就是将极坐标的信息转为直角坐标信息
        x = math.trunc((r * -250.0)*math.cos(angle + (-90.0*3.1416/180.0)))
        y = math.trunc((r * 250.0)*math.sin(angle + (-90.0*3.1416/180.0)))
        if y > -300 and y < 300 and x<300 and x>-300:
            cv2.line(frame,(x+300,y+300),(x+300,y+300),(0,0,255),2)
        # 角度增加
        angle= angle + data.angle_increment
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

# 初始化节点，'laser_listener'
# 代表开启一个进程！匿名参数也默认是这个
# 订阅的语句。需要订阅的话题，数据类型，回调函数
# 最后的队列，queue_size参数需要换为1，只接收最新的一个消息
def laser_listener():
    rospy.init_node('laser_listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan,callback,queue_size = 1)
    rospy.spin()

if __name__ == '__main__':
    laser_listener()

```
可以看到显示图像：
![激光雷达数据显示](LaserScan.png)