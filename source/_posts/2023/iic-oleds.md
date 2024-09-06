---
title: 一个iic通道控制多个相同地址的从设备
tags:
  - arduino
  - esp32
cover: /img/d5bd564e82238fa871150c9b3fe22c8.jpg
categories:
- 折腾记录
notshow: false
date: 2023-03-28 17:18:00
description: 一种类似spi片选功能的方法控制多个相同地址设备
---
## 前言
### 需求
一个小键盘，有四个按键，想要在每一个键帽上安装一个0.49寸的oled灯。主控使用esp32，如果直接使用软件iic，那么需要4个通道也就是8个引脚来控制。由于还有许多其他功能，导致io不足以如此挥霍。
### 解决方法
屏幕全部使用同一个iic通道。SCL时钟线接在一起，SDA数据线由主设备出发分别经过一个二极管连接到每个从设备。然后从设备的SDA经过一个pnp三极管连接到一个单片机io引脚。如果希望不修改这个屏幕的数据，就把这个从设备的引脚拉高，无法再接收数据，就可以实现单独控制。

## 实验
上电后两个屏幕都会在c和v之间循环切换，如果串口输入0，一个屏幕就会暂停，另一个屏幕正常闪烁，串口输入1恢复正常

顺便实测当字号使用24时候刷新时间是2500us左右，字号16的刷新时间大概是1600us，这个速度已经可以和foc的循环放在一个函数里了笑死(foc控制循环建议速度1kHz)
### 电路连接
![](d5bd564e82238fa871150c9b3fe22c8.jpg)
### 控制程序
```
#include <Wire.h>
#include "SSD1306.h"
SSD1306 display(0x3c, 22, 23);
String comStr = "";
long comInt=1;
void setup(){
  pinMode(21, OUTPUT);
  digitalWrite(21, HIGH);
  Serial.begin(115200);
  display.init();
  display.setFont(ArialMT_Plain_16);
  display.drawString(32, 0, "ctrl+v");
  display.display();
  while(Serial.read()>=0){}
}

void loop(){
  unsigned int time;
  time = micros();
  display.clear();
  display.drawString(32, 0, "ctrl+c");
  display.display();
  Serial.println(micros()-time);
  display.clear();
  display.drawString(32, 0, "ctrl+v");
  display.display();
  if (Serial.available() > 0){
    comStr = Serial.readString();
    comInt = comStr.toInt();
    if (comInt==0){digitalWrite(21, LOW);}
    if (comInt==1){digitalWrite(21, HIGH);}
  }
}

```