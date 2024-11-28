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
这个项目是我大学本科四年做的最复杂的一个，从大一下学期到大三结束一路磕磕绊绊走走停停终于到了可以写总结的时候，现在这个仅剩下一点无关紧要的收尾工作了。

{% note danger modern %}
警告：本文设计内容具有危险性，不提供任何制造文件资料，仅供科研交流使用，装置测试后已经拆除，严禁仿造用于其他用途。
{% endnote %}

说一下我的最终设计路线和目标：
+ 高压方案(>300V)
+ 快速连续工作(<1s)
+ 速度快(>100m/s)
+ 效率有追求但不很重要(>10%)

# Maxwell电磁力运动仿真
之前写的教程比较简略（晦涩难懂），步骤太多文字写起来很麻烦，直接录下来操作视频发b站了

视频中演示的结构为高压方案的单路boost拓扑，位置触发的时序控制，外电路激励源
{% raw %}
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113007065564118&bvid=BV168WEeBEmV&cid=500001658823200&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="position: absolute; width: 100%; height: 100%; Left: 0; top: 0;" ></iframe></div>
{% endraw %}

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

我还找到了一个maxwell的使用教程文档，不知道有没有用，因为太长了我没看，但是万一有人需要呢？

{% pdf MAXWELL基础教程电子版.pdf %}

## 功率电路

| ![](微信截图_20240719201740.png) | ![](微信截图_20240719202048.png) | ![](f6e19e7d493377e57490c1ba6c95cbc.jpg) | ![](fb16ed462e5e7065995940dd605b93f.jpg) |
|:---:|:---:|:---:|:---:|
| 功率板原理图 | 驱动板原理图 | 照片 | 效果 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> | <img width=2000/> |

线圈设计参数：

![](微信截图_20240719202940.png)

实测速度基本稳定在45m/s，如果连续使用线圈发热增加的电阻率会降低电流导致速度降低，实测温度到40度时速度会降低到40左右，因此未来的设计将会关注热管理问题。


## 时序控制

外接自制那个esp32开发板，代码在这里，时序使用循环计算，不再需要手动考虑高低电平切换顺序了，以及做了串口调参，节省一下flash的烧录寿命hhh

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

## ZVS升压电源
电源有多种方案，最简单的ZVS谐振逆变升压，十分简单但是不够可控可靠，无法控制工作状态，而且在负载过流情况下一旦停止谐振就会直接在电源上短路，如果使用电池供电十分危险，不过只要重新接入电源重新进入谐振状态就可以继续正常工作。另一种使用开关电路逆变升压，较为复杂但是可控。当然我们的需求是给电容充电，使用恒流源更合适，具体实现参考论文《一种谐振型推挽式直流变换器》

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

# n*5 LEVELS
## 电路设计
这次采用了模块化设计，每个板子是5级功率回路，可以直接串联使用

| ![](微信截图_20240910134109.png) | ![](微信截图_20240910134138.png) | ![](微信截图_20240910134204.png) |
| :---: | :---: | :---: |
| ![](微信截图_20240910134123.png) | ![](微信截图_20240910134148.png) | ![](微信截图_20240910134215.png) |
| 放电电路 | 驱动电路 | 供电主板 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> |


线圈设计参数：
![](微信截图_20240910134526.png)


## 时序控制
### 控制程序
考虑到esp32引脚数量不足，主控芯片更换为stm32。以及这次可以进行电压测量和充电电流监控并主动控制，加入了这部分控制代码

<details>
  <summary>一些吐槽</summary>
  这段代码实在是太不优雅了，真受不了这一堆if else，但是又一直懒得重构。。。至少暂时不耽误用。以及现在电压主动控制还没写，等写完了就删掉这句话
</details>

```c
//cxx: control[just a str], level, 0:duration/1:start time//2:end time

// start time
int c11_time = 0;
int c21_time = 1350;
int c31_time = 2000;
int c41_time = 2630;
int c51_time = 3100;
int c61_time = 3490;
int c71_time = 3830;
int c81_time = 4140;
int c91_time = 4410;
// duration
int c10_time = 1340;
int c20_time = 880;
int c30_time = 770;
int c40_time = 590;
int c50_time = 500;
int c60_time = 470;
int c70_time = 400;
int c80_time = 360;
int c90_time = 340;
// trigger status
const int c1 = 13;
const int c2 = 12;
const int c3 = 14;
const int c4 = 27;
const int c5 = 26;
const int c6 = 25;
const int c7 = 33;
const int c8 = 32;
const int c9 = 23;
const int sw = 0;
int serial_sw = 0;

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
  pinMode(c6, OUTPUT);
  pinMode(c7, OUTPUT);
  pinMode(c8, OUTPUT);
  pinMode(c9, OUTPUT);
  digitalWrite(c1, LOW);
  digitalWrite(c2, LOW);
  digitalWrite(c3, LOW);
  digitalWrite(c4, LOW);
  digitalWrite(c5, LOW);
  digitalWrite(c6, LOW);
  digitalWrite(c7, LOW);
  digitalWrite(c8, LOW);
  digitalWrite(c9, LOW);

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
      if (function=="shot"){
        serial_sw = 1;
        Serial.println("Shot after 1 second!");
        delay(1000);
      }

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
      }else if (function=="c51 "){
        String value_str = inData.substring(4, inData.length());
        c51_time = value_str.toInt();
        Serial.printf("Now c51 = ");
        Serial.println(c51_time);
      }else if (function=="c50 "){
        String value_str = inData.substring(4, inData.length());
        c50_time = value_str.toInt();
        Serial.printf("Now c50 = ");
        Serial.println(c50_time);
      }else if (function=="c61 "){
        String value_str = inData.substring(4, inData.length());
        c61_time = value_str.toInt();
        Serial.printf("Now c61 = ");
        Serial.println(c61_time);
      }else if (function=="c60 "){
        String value_str = inData.substring(4, inData.length());
        c60_time = value_str.toInt();
        Serial.printf("Now c60 = ");
        Serial.println(c60_time);
      }else if (function=="c71 "){
        String value_str = inData.substring(4, inData.length());
        c71_time = value_str.toInt();
        Serial.printf("Now c71 = ");
        Serial.println(c71_time);
      }else if (function=="c70 "){
        String value_str = inData.substring(4, inData.length());
        c70_time = value_str.toInt();
        Serial.printf("Now c70 = ");
        Serial.println(c70_time);
      }else if (function=="c81 "){
        String value_str = inData.substring(4, inData.length());
        c81_time = value_str.toInt();
        Serial.printf("Now c81 = ");
        Serial.println(c81_time);
      }else if (function=="c80 "){
        String value_str = inData.substring(4, inData.length());
        c80_time = value_str.toInt();
        Serial.printf("Now c80 = ");
        Serial.println(c80_time);
      }else if (function=="c91 "){
        String value_str = inData.substring(4, inData.length());
        c91_time = value_str.toInt();
        Serial.printf("Now c91 = ");
        Serial.println(c91_time);
      }else if (function=="c90 "){
        String value_str = inData.substring(4, inData.length());
        c90_time = value_str.toInt();
        Serial.printf("Now c90 = ");
        Serial.println(c90_time);
      }
      inData="";
    }

  }

  // switch
  if (digitalRead(sw)==LOW||serial_sw){
    // reset
    serial_sw = 0;
    int c11 = 1;
    int c21 = 1;
    int c31 = 1;
    int c41 = 1;
    int c51 = 1;
    int c61 = 1;
    int c71 = 1;
    int c81 = 1;
    int c91 = 1;
    int c12 = 1;
    int c22 = 1;
    int c32 = 1;
    int c42 = 1;
    int c52 = 1;
    int c62 = 1;
    int c72 = 1;
    int c82 = 1;
    int c92 = 1;
    int c12_time = c11_time + c10_time;
    int c22_time = c21_time + c20_time;
    int c32_time = c31_time + c30_time;
    int c42_time = c41_time + c40_time;
    int c52_time = c51_time + c50_time;
    int c62_time = c61_time + c60_time;
    int c72_time = c71_time + c70_time;
    int c82_time = c81_time + c80_time;
    int c92_time = c91_time + c90_time;
    Serial.println("starting");
    pulseStartTime = micros();
    pulseNowTime = micros();
    while(c11||c12||c21||c22||c31||c32||c41||c42||c51||c52||c61||c62||c71||c72||c81||c82||c91||c92){
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
      
      if(pulseNowTime-pulseStartTime>c51_time && c51){
        digitalWrite(c5, HIGH);
        c51 = 0;}
      if(pulseNowTime-pulseStartTime>c52_time && c52){
        digitalWrite(c5, LOW);
        c52 = 0;}
      
      if(pulseNowTime-pulseStartTime>c61_time && c61){
        digitalWrite(c6, HIGH);
        c61 = 0;}
      if(pulseNowTime-pulseStartTime>c72_time && c62){
        digitalWrite(c6, LOW);
        c62 = 0;}
      
      if(pulseNowTime-pulseStartTime>c71_time && c71){
        digitalWrite(c7, HIGH);
        c71 = 0;}
      if(pulseNowTime-pulseStartTime>c72_time && c72){
        digitalWrite(c7, LOW);
        c72 = 0;}
      
      if(pulseNowTime-pulseStartTime>c81_time && c81){
        digitalWrite(c8, HIGH);
        c81 = 0;}
      if(pulseNowTime-pulseStartTime>c82_time && c82){
        digitalWrite(c8, LOW);
        c82 = 0;}

      if(pulseNowTime-pulseStartTime>c91_time && c91){
        digitalWrite(c9, HIGH);
        c91 = 0;}
      if(pulseNowTime-pulseStartTime>c92_time && c92){
        digitalWrite(c9, LOW);
        c92 = 0;}


      if(pulseNowTime-pulseStartTime>1000000){
        Serial.print("ERROR, time out");
        break;
      }
    }
    // not release
    //Serial.println("releasing");

    //digitalWrite(c5, HIGH);
    delay(2000);
    //digitalWrite(c5, LOW);
    Serial.println("finished");
  }
}

```
### 电磁运动仿真计算
maxwell计算结果和coilgun RLC基本一致，但是出现了一些新的问题，由于线圈电流的巨大变化率，会在相邻线圈产生感生电流，可能导致IGBT过压击穿，因此本来计划做15级破百，由于11-15级匝数更少电流更大产生的感生电流过大，因此打算只做10级，速度只能达到70-80。解决这个问题需要改成多路boost，需要重新设计PCB，所以等下一版本再说吧

经过计算发现，最佳的开启和关断位置是固定的，这一次仿真已经是完全由位置触发得到的了，效果非常好，甚至可以用于估算代码设置的延迟时间

| ![](Speed.png) | ![](Winding.png) | ![](NodeVoltage.png) |
| :---: | :---: | :---: |
| 运动参数 | 线圈电流 | 电容电压 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> |

但是线圈电流仿真结果显示线圈匝数的设计还有优化空间，关断时的电流过大，降低了效率和IGBT可靠性

[Maxwell仿真文件](DCP_maxwell.7z)

### 设计优化
对于线圈，首先应该用较大的匝数进行初始的加速，然后随着速度增加，线圈导通的时间越来越短，因此需要减少电感量来提高响应速度，即减少匝数。因此后级最佳的匝数应逐级减少。

当IGBT关断时，线圈的电流应该已经过了峰值，并且降低的足够低，这样可以降低电容剩余电压，提高加速度。因此可以根据关断时的电流值确定合适的匝数。如果刚过峰值就关断，就减少线圈的匝数。应该比较好的关断时机是电流峰值的2/3到1/2

当速度达到接近100时，由于匝数很小可能导致电感过小电流过大，此时可以降低电容容量，降低峰值电流避免IGBT出现故障

对于磁阻结构，能量的损耗在于电阻发热和磁场加速损耗，线圈使用更大的线径可以降低电阻，进一步提高效率。实际制造中，更粗的线圈会极大提高手工绕制难度，因此我自己的方案仍然使用0.45mm直径

线圈直径越大，在缝隙处的损耗就会占比更小，因此拥有更高的效率，我也因此把定位销尺寸从m6改为m8。为了减少缝隙的磁场损耗，缝隙处从1mm厚度的abs和1mm厚度线轴改为0.5mm的不锈钢缠绕高温胶带绝缘。减少缝隙可以极大提高效率。

根据其他人的实验，AUIRGPS4067D的峰值电流在驱动电压正20负5时，520V560uf100uh大概每隔30s放电一次，800A450us关断，极限测试了50次没有问题。不过保守使用3-500A应该不会有问题

### 推挽升压电源
这种方案使用芯片产生的指定频率的互补的PWM波形控制MOS推挽升压，至少不会停振短路了。我用的是SG3525产生信号然后UCC27324驱动MOS，经过变压器升压，整流后输出高压直流。为了及时关断，使用单片机采集电压控制开关

### 全桥恒流谐振
直接上论文：

{% pdf 一种谐振型推挽式直流变换器_袁义生.pdf %}

# 特别感谢

[科创网](https://www.kechuang.org/f/367)
[JLC](https://www.jlc.com/)
**QQX**
