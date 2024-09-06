---
title: 在极坐标下参考DBSCAN的聚类算法
date: 2022-10-28 11:03:04
tags:
- python
- opencv
- ROS
- 笔记
description: 根据激光雷达的数据特点对DBSCAN聚类算法进行修改
cover: /img/LaserScan-DBSCAN-PolarCoordinates.png
categories: 
- [折腾记录]
- [作品&项目总结]
---
## DBSCAN聚类算法
有一个对这个算法进行[可视化的网站](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/ "可视化的网站")
我们将激光雷达识别到的点进行聚类来识别不同物体
## 前言
之所以不直接使用上述算法，是因为激光雷达的是极坐标下的数据，而且同一个角度的点只会有一个。所以这里借用上述算法的思路，做一个激光雷达专用的聚类算法。
## 代码
```python
import rospy
import cv2
import numpy as np
import math
from sensor_msgs.msg import LaserScan

def callback(data):
    # 参数设置
    ab = 200    # 雷达可视化画面缩放，数值越小可视范围越广
    ba = 800    #可视化界面边长
    points_range = 10   # 聚类点云范围
    points_amount = 5   # 聚类点数量最小值
    max_distance = 0.15 # 同类点最大距离

    ba2 = int(ba/2)
    # 雷达绘图
    frame = np.zeros((ba, ba,3), np.uint8)
    angle = data.angle_min
    cv2.circle(frame, (ba2,ba2), 5, (255,255,255), -1)
    for r in data.ranges:
        if math.isinf(r) == True:
            r = 1000
        #将极坐标的信息转为直角坐标信息
        x = math.trunc((r * -ab)*math.cos(angle + (-90.0*3.1416/180.0)))
        y = math.trunc((r * ab)*math.sin(angle + (-90.0*3.1416/180.0)))
        if y > -ba2 and y < ba2 and x < ba2 and x > -ba2:
            # 用CV2画线
            cv2.line(frame,(x+ba2,y+ba2),(x+ba2,y+ba2),(0,0,255),2)
        # 角度增加
        angle= angle + data.angle_increment

    out = [0] * 1440    #激光雷达每一圈采集1440个点
    #聚类
    for i in range(0,int(len(data.ranges)-1-points_range)):
        p = 0
        for j in range(1,points_range+1):
            if abs(data.ranges[i+1]-data.ranges[i+j+1])<=max_distance:
                p = p + 1
            if p>=points_amount:
                for k in range(i,i+j+1):
                    out[k] = 1
    print(out)  #此时输出的是只有0，1的列表，其中1表示有障碍物。
    #连续1检测
    p = 0
    out11 = []
    for i in range(1,len(out)-2):
        if out[i]==1 and out[i-1]==0:
            p = p + 1
            k = i
        if out[i]==1 and out[i+1]==0:
            out11.append([k,i])
        if out[i]==1:
            out[i]=p
    print(out)  #此时out输出给所有障碍物编号后的结果
    print(out11)    #每个障碍物角度范围的二维数组
    #聚类效果可视化为绿点
    for i in out11:
        total = 0
        total1 = 0
        for j in range(i[0],i[1]):
            if math.isinf(data.ranges[j]) == False and data.ranges[j]>0.1:
                total = total + data.ranges[j]
                total1 = total1 + 1
        r = total / total1
        angle = data.angle_min + data.angle_increment * round((i[0]+i[1])/2)
        x = math.trunc((r * -ab)*math.cos(angle + (-90.0*3.1416/180.0)))
        y = math.trunc((r * ab)*math.sin(angle + (-90.0*3.1416/180.0)))
        if y > -ba2 and y < ba2 and x < ba2 and x > -ba2:
            cv2.line(frame,(x+ba2,y+ba2),(x+ba2,y+ba2),(0,255,0),5)
            print([x,y])

    cv2.imshow('frame',frame)
    cv2.waitKey(1)

# 初始化节点'laser_listener'
# 代表开启一个进程
# 订阅:需要订阅的话题，数据类型，回调函数
# 最后的队列queue_size参数需要换为1，只接收最新的一个消息
def laser_listener():
    rospy.init_node('laser_listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan,callback,queue_size = 1)
    rospy.spin()

if __name__ == '__main__':
    laser_listener()

```