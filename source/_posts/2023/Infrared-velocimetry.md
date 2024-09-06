---
title: 红外测速
tags:
  - PCB设计
cover: /img/RUN.png
categories:
- [过时&弃用&无意义&失败品]
- [折腾记录]
date: 2023-10-15 16:20:01
description: Infrared-velocimetry
---
# 需求
我想要在不接触的情况下测量一个小玻璃弹珠的速度，最开始买了几个常用的红外管结果发现触发性能不达标，速度在3m/s以上时就会无法检测到。首先要高速，最好能测量几十米每秒的速度，然后最好便携一点

# 方案
找了一个看起来不错的光电管`IR12-21C/TR8`和`PT12-21B/TR8`，价格也很感人就是了，然后前后两个板子用同一个PCB，板对板连接，然后连接到外置的单片机

# PCB
| ![](微信截图_20231015162424.png)  | ![](微信截图_20231015162438.png)  | ![](微信截图_20231015162455.png)  |
| :------------: | :------------: | :------------: |
| 原理图  | PCB  | 3D模型  |

# 程序

```c
unsigned long t12 = 0;
unsigned long t13 = 0;
int trigger = 0;

void IRAM_ATTR isr12() {
  t12 = micros();
  trigger = 12;
}

void IRAM_ATTR isr13() {
  t13 = micros();
  trigger = 13;
}

void setup() {
	Serial.begin(115200);
	pinMode(12, INPUT_PULLUP);
  pinMode(13, INPUT_PULLUP);
	attachInterrupt(12, isr12, RISING);
  attachInterrupt(13, isr13, RISING);
}

void loop() {
	if (trigger == 13){
		Serial.print("trigger13:");
    Serial.println(t13-t12);
    Serial.print("-----v:");
    Serial.print(5600000/(t13-t12));
    Serial.println("cm/s");
		trigger = 0;
	}else if(trigger == 12){
    Serial.print("trigger12:");
    Serial.print(t12-t13);
    Serial.print("-----v:");
    Serial.print(5600000/(t12-t13));
    Serial.println("cm/s");
		trigger = 0;
  }
}
```
通过这个程序发现实际使用过程中，有时候会出现同一位置两次触发，暂时不确定是因为振铃还是因为物体长度。考虑到物体长度减小触发间隔减小，我认为应该是物体长度导致的变化
![](QQ截图20231103233139.png)
