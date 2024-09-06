---
title: 使用ardupilot的四轴飞行器
tags:
  - arduino
cover: /img/slides_01_Ardupilot42.webp
categories:
- [折腾记录]
- [作品&项目总结]
notshow: false
date: 2023-05-17 22:33:16
description: 晚上心血来潮随手搓个四轴玩
---
# ArduPilot
[ArduPilot is a trusted, versatile, and open source autopilot system supporting many vehicle types: multi-copters, traditional helicopters, fixed wing aircraft, boats, submarines, rovers and more. The source code is developed by a large community of professionals and enthusiasts. New developers are always welcome! The best way to start is by joining the Developer Team Forum, which is open to all and chock-full of daily development goodness](https://ardupilot.org/)

# 软件安装及配置
## 软件资源下载
[地面站下载](https://cr.triority.cn/f/J0PsK/MP1.3.28.msi)
[飞控固件下载](https://cr.triority.cn/f/p5KIk/ardupilot.rar)

## minim OSD显示配置


# 硬件连接结构
## 飞控接线图
![](20190107165026890.jpg)

## 电机和桨叶方向
![](f9e979ae8c0ee89fe689f15214c04bd.jpg)

不仅是电调接线顺序，务必注意电机旋转方向，否则起飞即自转

## GPS方向
GPS箭头方向必须与飞控相同，否则定点飞行将会发生持续漂移

## 机架1.0
最开始用的现成的机架，后来炸鸡摔断了，于是自己3D打印设计了一整个来满足消耗，目前画的这些，反正终稿肯定还要改很多

![目前装配体长这样](QQ截图20230605143807.png)

[solidworks文件下载链接](apm2.8机架.rar)

## 机架2.0
这次机架改进了很多，首先是集成了所有电控部分在中间的长方体里，同时考虑到便携性，四个电机支架可以用手拧螺丝直接拆装，电池部分也改成扎带绑在上面，下部空出位置放置相机云台等。不过由于这个结构，机身重量也增加了三五十克。

{% dplayer "url=https://cr.triority.cn/f/vzZIl/1686471126438.mp4" %}

