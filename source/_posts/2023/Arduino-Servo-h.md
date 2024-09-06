---
title: Arduino舵机库控制舵机和无刷电调
tags:
  - arduino
cover: /img/ff589b65d94461294ee7c69f4bd4eef.jpg
categories:
- 折腾记录
notshow: false
date: 2023-02-24 21:56:43
description: arduino舵机库的使用
---
# 注意事项
当在UNO使用`<Servo.h>`时，由于占用的9和10号数字引脚的PWM定时器，因此它们无法使用`analogWrite()`语句。但是可以接作为舵机控制信号引脚。其他型号详见各自文档。

# 使用<Servo.h>控制舵机
有两种控制方法，一种是直接定角度控制，一种是更加准确通用的脉宽控制。后面控制无刷电调的程序使用的就是脉宽控制方式。所以这里只写角度控制。
```
#include <Servo.h>

Servo myServo;

String comStr = "";
int comInt=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(Serial.read()>=0){} // clear serial port's buffer
  
  myServo.attach(9); // attach myServo to GPIO_09
  myServo.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    // listen the Serial port, run the code when something catched..
    delay(50);
    comStr = Serial.readString(); // read out the string
    comInt = comStr.toInt(); // convert the string to integer
    comInt = constrain(comInt, 0, 180); // between to 0 and 180
    Serial.println(comInt);
    
    myServo.write(comInt);
    
  }
  
}

```

# 使用<Servo.h>控制无刷电机电调
可使用串口发送`1000-2000`控制速度。

电调所期望的控制信号通常是频率为50Hz的PWM信号，通过占空比来控制“油门”的大小，1ms高电平为电调识别的最低“油门”（转速0%,PWM50%），2ms高电平则为最高可识别的“油门”（转速100%,PWM100%）。

第一次开机时需要对电调进行校准，具体校准流程如下：
+ 正常电调上电提示音是do re mi, 哔哔哔 哔~，100%油门的设置要在哔~之前操作，否则电调会直接进入正常上电状态，而不会进入校准模式
+ 油门设置到100%等待2s(哔哔两声)
+ 油门设置到0%等待1s(哔一声)
+ 油门全行程校准完成

```
#include <Servo.h>

Servo myServo;

String comStr = "";
int comInt=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(Serial.read()>=0){} // clear serial port's buffer
  
  myServo.attach(9); // attach myServo to GPIO_09
  myServo.writeMicroseconds(1000); // set initial PWM to minimal
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    // listen the Serial port, run the code when something catched..
    delay(10);
    comStr = Serial.readString(); // read out the string
    comInt = comStr.toInt(); // convert the string to integer
    comInt = constrain(comInt, 1000, 2000); // limit the integer between to 1000 and 2000

    Serial.println(comInt); // show the integer number on Serial Monitor
    myServo.writeMicroseconds(comInt); // write the integer number to Servo in unit of micro-second
    
  }
  
}

```
