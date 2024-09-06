---
title: 延时摄影图片合成视频
date: 2022-07-08 11:30:40
tags:
- python
- opencv
- 3D打印
description: 重写了之前用的程序...
cover: /img/photos2video.png
categories: 
- 旅游&摄影
---
## 前言
在[之前的文章](http://triority.cn/2022/05/17/arduino-voltmeter/#%E6%AF%8F%E5%B1%82%E7%85%A7%E7%89%87%E5%90%88%E6%88%90%E8%A7%86%E9%A2%91 "之前的文章")里，我找了用一个python程序把延时摄影的很多张照片合成视频，那个时候用来合成树莓派摄像头拍的几百张照片问题不大，但是今天尝试合成手机拍的照片，瞬间内存爆满，一看代码，气死个人，把所有照片存进一个数组再从数组里一个个取出来写入视频，搁这搁这呢属于是，所以自己重写一个，顺便去掉文件名限制，直接默认排序
## 程序
直接读取图片写入视频，内存占用就下来了
```python
import cv2
import os

photos = os.listdir(r'cam_3D')
photo = cv2.imread('cam_3D\\' + photos[0])
size = (photo.shape[1], photo.shape[0])
videowrite = cv2.VideoWriter(r'test.mp4', -1, 30, size)
i=0
for filename in photos:
    path = 'cam_3D\\' + filename
    img = cv2.imread(path)
    if img is None:
        print(filename + " is error!")
        continue
    videowrite.write(img)
    i += 1
    print(i)
videowrite.release()
print('finished')
```