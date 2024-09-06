---
title: 在智能车航天组中的视觉识别赛道并拟合数据
date: 2022-1-28 21:33:39
tags:
- python
- opencv
description: 在智能车航天组中的视觉识别赛道并拟合数据
cover: /img/opencv-for-Aerospace.png
categories: 
- [折腾记录]
- [值得一提的文章]
---
## 在智能车航天组中的视觉识别赛道
```python
import numpy as np
import cv2
#定义HSV颜色选取范围
color_dist = {'Lower': np.array([100, 50, 10]), 'Upper': np.array([130, 150, 150])}
#读取视频文件
cap = cv2.VideoCapture(r'E:\car\航天智慧物流-线上赛规则\五个关键技术任务\03. 计算机视觉\视觉任务\测试数据\1-主场景\camtest.mp4')
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    frame2=frame.copy()
    frame = frame[-150:-1, 1:910]
    #高斯滤波降噪
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    #RGB转HSV并进行处理
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=2)
    #将HSV图像二值化处理
    inRange_hsv = cv2.inRange(erode_hsv, color_dist['Lower'], color_dist['Upper'])
    #获取二值化图像轮廓
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #存储轮廓
    target_list = []
    x=[]
    y=[]
    for c in cnts:
        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 1500:  # 过滤小面积
            continue
        else:
            target_list.append(c)
    #获取轮廓中心点
    for i in target_list:
        M = cv2.moments(i)  # 计算中心点的x、y坐标
        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])
        x.append(center_x)
        y.append(center_y)

        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        cv2.drawContours(frame2, [np.int0(box)], -1, (0, 255, 255), 2)
    #拟合散点
    if len(target_list) > 2 :
        x=np.array(x)
        z1 = np.polyfit(y, x, 2)  # 用2次多项式拟合
    elif len(target_list) == 2 :
        x=np.array(x)
        z1 = np.polyfit(y, x, 1)  # 用1次多项式拟合
    else :
        z1 = 0
    p1 = np.poly1d(z1)
    #显示拟合曲线
    if len(target_list) >= 2 :
        for i in range(1,frame.shape[0]-1):
            cv2.line(frame2, (round(p1(i)), i+390), (round(p1(i+1)),i+391), (255, 0, 0), 3)
        fx=str(p1)
        cv2.putText(frame2, fx, (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.waitKey(1)
    #创建窗口播放视频
    cv2.imshow('2',frame2)
    #cv2.imshow('1', frame)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()

```