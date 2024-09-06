---
title: 电磁炉：使用H桥能量回收
tags:
  - 电磁炉
  - 电力电子
  - PCB设计
cover: /img/v2-100f3b14743b9c8fe3e58536acaa072c_r.png
categories:
- 折腾记录
date: 2023-1-18 12:56:17
description: 使用IGBT控制的H桥电路回收电感能量
---
# 概述
使用H电路原理大概就是IGBT导通线圈放电，关断时线圈通过二极管把电能充回电容。这样可以达到让电感电流衰减最快，反拉效应最小，同时能量回收提高效率，缩短下次充电时间

电路图大致就是这样：
![电路图](fbq.png)

这个电路需要同时导通上下IGBT管，而且控制上比较复杂等单个IGBT做明白了再说

# 开工
总之就是本来想先做单个igbt可控关断的，结果10.13发现因为igbt电流比较小前几级效果甚至不如晶闸管的，但是半桥回收的方案在后面几级效率太强了，碰巧刷到一个半桥芯片`eg3116D`没有闭锁可以同时导通上下半桥，所以直接就给板子做了

目前完成的设计是这样的：

| ![](QQ截图20231014004719.png)  | ![](QQ截图20231014004745.png)  | ![](QQ截图20231013180823.png)  |
| :------------: | :------------: | :------------: |
| 原理图  | PCB  | 3D模型  |

3D模型那个电容重叠是因为要兼容1个1000uf电容和最多4个220uf的电容，节约点高度(不然高度10cm以上了你懂的)

等板子到了再更新效果

程序：
```
void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);
  pinMode(0,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(0)==LOW){
    digitalWrite(13, HIGH);
    delayMicroseconds(1200);
    digitalWrite(13, LOW);
    delay(2000);
  }
}
```
