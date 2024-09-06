---
title: 超高速直线电机
tags:
  - 电力电子
  - PCB设计
cover: /img/微信截图_20240720191614.png
categories:
  - 值得一提的文章
  - 折腾记录
  - 作品&项目总结
date: 2024-07-02 21:37:22
description: 高功率高压高速直线电机
---
# 概述
这个项目是我大学本科四年做的最复杂的一个，从大一下学期到大三结束一路磕磕绊绊走走停停终于到了可以写总结的时候。

{% note danger modern %}
警告：本文设计内容具有危险性，不提供任何制造文件资料，仅供科研交流使用，装置测试后已经拆除，严禁仿造用于其他用途。
{% endnote %}

说一下我的最终设计路线和目标：
+ 高压方案(>300V)
+ 快速连续工作(<1s)
+ 速度快(>100m/s)
+ 效率有追求但不很重要(>10%)

# 4 LEVELS
## 基本参数

+ 加速体：A3材质M8x20圆柱定位销
+ 轨道：内8.5外9.5钢管
+ 电压：350V
+ 拓扑：boost
+ IGBT：IRGPS4067d
+ 线圈：0.45mm漆包铜线

## Ansys Maxwell仿真

{% dplayer "url=baaf983f8c3aca6c53c2238da466f09d.mp4" %}

| ![](a39d70ac42f5250a742b76c01ecb0b3.png) | ![](16358072e8a10c489cf6da88cacde99.png) | ![](a77a7f8f7a4bb36dd2e99821d910b03.png) | ![](69911deecbd0ee65e2049c05d23a9d8.png) | ![](86de12335351f9e49a989d161d67152.png) |
|:---:|:---:|:---:|:---:|:---:|
| 实体模型 | 电路模型 | 电流 | 拉力 | 速度 |

[仿真工程文件](DCP_maxwell.zip)

## 功率电路

| ![](微信截图_20240719201740.png) | ![](微信截图_20240719202048.png) | ![](f6e19e7d493377e57490c1ba6c95cbc.jpg) | ![](fb16ed462e5e7065995940dd605b93f.jpg) |
|:---:|:---:|:---:|:---:|
| 功率板原理图 | 驱动板原理图 | 照片 | 效果 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> | <img width=2000/> |

线圈设计参数：

![](微信截图_20240719202940.png)

实测速度基本稳定在45m/s，如果连续使用线圈发热增加的电阻率会降低电流导致速度降低，实测温度到40度时速度会降低到40左右，因此未来的设计将会关注热管理问题。

代码在这里，时序使用循环计算，不再需要手动考虑高低电平切换顺序了，以及做了串口调参，节省一下flash的烧录寿命hhh

```c
//cxx: control[just a str], level, 0:duration/1:start time//2:end time

// start time
int c11_time = 0;
int c21_time = 1650;
int c31_time = 2400;
int c41_time = 2950;
// duration
int c10_time = 1460;
int c20_time = 840;
int c30_time = 670;
int c40_time = 580;

// trigger status
const int c1 = 26;
const int c2 = 27;
const int c3 = 14;
const int c4 = 12;
const int c5 = 13;
const int sw = 0;

unsigned long pulseStartTime = 0;
unsigned long pulseNowTime = 0;

String inData="";

void setup() {
  Serial.begin(115200);
  pinMode(c1, OUTPUT);
  pinMode(c2, OUTPUT);
  pinMode(c3, OUTPUT);
  pinMode(c4, OUTPUT);
  pinMode(c5, OUTPUT);
  digitalWrite(c1, LOW);
  digitalWrite(c2, LOW);
  digitalWrite(c3, LOW);
  digitalWrite(c4, LOW);
  digitalWrite(c5, LOW);

  pinMode(sw, INPUT);
}

void loop() {
  // serial
  while(Serial.available()>0){
    delay(5);
    char recieved = Serial.read();
    inData += recieved;
    if(recieved == '\n'){
      if (inData.length()<4){
        Serial.println("Too short");
        break;
      }
      String function = inData.substring(0, 4);

      if (function=="c11 "){
        String value_str = inData.substring(4, inData.length());
        c11_time = value_str.toInt();
        Serial.printf("Now c11 = ");
        Serial.println(c11_time);
      }else if (function=="c10 "){
        String value_str = inData.substring(4, inData.length());
        c10_time = value_str.toInt();
        Serial.printf("Now c10 = ");
        Serial.println(c10_time);
      }else if (function=="c21 "){
        String value_str = inData.substring(4, inData.length());
        c21_time = value_str.toInt();
        Serial.printf("Now c21 = ");
        Serial.println(c21_time);
      }else if (function=="c20 "){
        String value_str = inData.substring(4, inData.length());
        c20_time = value_str.toInt();
        Serial.printf("Now c20 = ");
        Serial.println(c20_time);
      }else if (function=="c31 "){
        String value_str = inData.substring(4, inData.length());
        c31_time = value_str.toInt();
        Serial.printf("Now c31 = ");
        Serial.println(c31_time);
      }else if (function=="c30 "){
        String value_str = inData.substring(4, inData.length());
        c30_time = value_str.toInt();
        Serial.printf("Now c30 = ");
        Serial.println(c30_time);
      }else if (function=="c41 "){
        String value_str = inData.substring(4, inData.length());
        c41_time = value_str.toInt();
        Serial.printf("Now c41 = ");
        Serial.println(c41_time);
      }else if (function=="c40 "){
        String value_str = inData.substring(4, inData.length());
        c40_time = value_str.toInt();
        Serial.printf("Now c40 = ");
        Serial.println(c40_time);
      }
      inData="";
    }

  }

  // switch
  if (digitalRead(sw)==LOW){
    // reset
    int c11 = 1;
    int c21 = 1;
    int c31 = 1;
    int c41 = 1;
    int c12 = 1;
    int c22 = 1;
    int c32 = 1;
    int c42 = 1;
    int c12_time = c11_time + c10_time;
    int c22_time = c21_time + c20_time;
    int c32_time = c31_time + c30_time;
    int c42_time = c41_time + c40_time;
    Serial.println("starting");
    pulseStartTime = micros();
    pulseNowTime = micros();
    while(c11||c12||c21||c22||c31||c32||c41||c42){
      pulseNowTime = micros();
      if(pulseNowTime-pulseStartTime>c11_time && c11){
        digitalWrite(c1, HIGH);
        c11 = 0;}
      if(pulseNowTime-pulseStartTime>c12_time && c12){
        digitalWrite(c1, LOW);
        c12 = 0;}

      if(pulseNowTime-pulseStartTime>c21_time && c21){
        digitalWrite(c2, HIGH);
        c21 = 0;}
      if(pulseNowTime-pulseStartTime>c22_time && c22){
        digitalWrite(c2, LOW);
        c22 = 0;}

      if(pulseNowTime-pulseStartTime>c31_time && c31){
        digitalWrite(c3, HIGH);
        c31 = 0;}
      if(pulseNowTime-pulseStartTime>c32_time && c32){
        digitalWrite(c3, LOW);
        c32 = 0;}

      if(pulseNowTime-pulseStartTime>c41_time && c41){
        digitalWrite(c4, HIGH);
        c41 = 0;}
      if(pulseNowTime-pulseStartTime>c42_time && c42){
        digitalWrite(c4, LOW);
        c42 = 0;}

      if(pulseNowTime-pulseStartTime>1000000){
        Serial.print("ERROR, time out");
        break;
      }
    }
    Serial.println("releasing");

    digitalWrite(c5, HIGH);
    delay(2000);
    digitalWrite(c5, LOW);
    Serial.println("finished");
  }
}

```

## 电源
电源有多种方案，最简单的ZVS谐振逆变升压，十分简单但是不够可控可靠，无法控制工作状态，而且在负载过流情况下一旦停止谐振就会直接在电源上短路，如果使用电池供电十分危险，不过只要重新接入电源重新进入谐振状态就可以继续正常工作。另一种使用开关电路逆变升压，较为复杂但是可控。当然我们的需求是给电容充电，使用恒流源更合适，具体实现参考论文《一种谐振型推挽式直流变换器》

### ZVS升压
不知道为什么这个电路被称为ZVS(零电压开关)电路，这只是一个恰好工作在零电压开关状态的谐振电路，不过这个名称和电路十分经典广为流传和使用，甚至淘宝所售套件的电源全都是这个方案，而且也足够简单，非常容易做

| ![](微信图片_20231022221839_1.jpg) | ![](微信图片_20231022221839.jpg) | ![](微信图片_20231022221839_2.jpg) | ![](微信图片_20231022221839_3.jpg) |
| :---: | :---: | :---: | :---: |
| 洞洞板试验 | 输入 | 波形 | 输出 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> | <img width=2000/> |

|![](微信截图_20240704130314.png)| ![](微信截图_20240704130544.png) | ![](微信图片_20231113160735.jpg) |
|:---:|:---:|:---:|
| 原理图 | 3D模型 | 照片 |

缺失模型的元件是电感和变压器。电感一定要电流足够大，分享一下我的电感和变压器选型吧

| ![](80744d6641f6b1eeb3cd457683ebc8e.jpg) | ![](055435e79723270fdaf48b5150b58e2.jpg) | ![](11fc579bfb3f5c95989dac205c9dcf4.jpg) |
| :---: | :---: | :---: |
| 电感 | 现在用的电容 | 打算以后换的电容 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> |

这个电路的问题我也说过了，就是一旦过载停振就会短路，所以我在前面加了一个PMos控制电源开关，短路可以及时关闭和重启。

### 开关电源
这种方案使用芯片产生的指定频率的互补的PWM波形控制MOS推挽升压，至少不会停振短路了。我用的是SG3525产生信号然后UCC27324驱动MOS，经过变压器升压，整流后输出高压直流。为了及时关断，使用单片机采集电压控制开关

### 全桥恒流谐振
直接上论文：

{% pdf 一种谐振型推挽式直流变换器_袁义生.pdf %}

# 特别感谢

[科创网](https://www.kechuang.org/f/367)
[JLC](https://www.jlc.com/)
**QQX**
