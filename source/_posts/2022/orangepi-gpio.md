---
title: orangepi-gpio
date: 2022-09-26 19:25:13
tags:
- 香橙派
- linux
- python
description: 香橙派GPIO的简单用法
cover: /img/香橙派zero2.png
categories: 
- 折腾记录
---
## 编译安装wiringOP
```
git clone https://github.com/orangepi-xunlong/wiringOP
cd wiringOP
./build clean
./build
```
## 测试
读取全部引脚：
```
gpio readall
```
## 在python中使用
```
>>> os.system("gpio read 2")
1
0
>>> os.system("gpio read 2")
0
0
```
## 一些其他语法
设置模式：
```
gpio mode 2 in
```
控制输出：
```
gpio write 2 0
```
## 废话结束
当然了做这个的目的是当GPIO引脚为低电平时下载保存esp32-cam拍摄的照片
```
import os
import time
import urllib.request
i=1
os.system("gpio mode 2 in")
while True and os.popen("gpio read 2").read().splitlines()[0]=='0':
    print ("starting")
    time.sleep(0.3)
while True:
    if os.popen("gpio read 2").read().splitlines()[0]=='0':
        print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
        print(i)
        urllib.request.urlretrieve("http://192.168.1.109/capture?_cb=1664116597682","cam/%s.jpg" % i)
        #camera.capture('/home/pi/Desktop/cam_3D/cam_3D/image%s.jpg' % i)
        urllib.request.urlretrieve("http://192.168.1.109/control?var=framesize&val=10","Resolution")
        i=i+1
        time.sleep(3)
    time.sleep(0.3)
    print("waiting")
```