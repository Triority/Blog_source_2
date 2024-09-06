---
title: 使用arduino的两轮自平衡车
tags:
  - arduino
cover: /img/
categories:
- [折腾记录]
- [作品&项目总结]
notshow: false
date: 2023-02-25 23:28:44
description: 使用arduino的同轴麦轮自平衡车
---
## 前言
原计划这个是用在rm里的麦轮平衡车，但是后来rm鸽子了也就懒得做麦轮了，但是刚好校赛剩下的零件可以做个两轮的车子于是就有了做个
## 获取imu传感器数据
#### 读取imu:mpu6050
[`MPU6050_tockn`库](https://github.com/tockn/MPU6050_tockn)获取角度的示例代码：
```
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  mpu6050.update();
  Serial.print("angleX : ");
  Serial.print(mpu6050.getAngleX());
  Serial.print("\tangleY : ");
  Serial.print(mpu6050.getAngleY());
  Serial.print("\tangleZ : ");
  Serial.println(mpu6050.getAngleZ());
}

```
#### 使用vofa+的tcp连接进行角度可视化
由于我们使用esp32因此可以连接wifi与电脑通讯而无需数据线，这里我们让esp32做服务端，电脑做客户端
```
#include <MPU6050_tockn.h>
#include <Wire.h>
#include <WiFi.h>

const char *ssid = "BJZQ";
const char *password = "12345678";
MPU6050 mpu6050(Wire);
WiFiServer server(80);

void setup() {
  pinMode(27, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  ledcSetup(8, 50, 8);
  digitalWrite(32, HIGH);
  digitalWrite(33, LOW);
  digitalWrite(25, HIGH);
  digitalWrite(26, LOW);
  ledcAttachPin(27, 8);
  ledcWrite(8, 120);
  ledcSetup(6, 50, 8);
  ledcAttachPin(14, 6);
  ledcWrite(6, 120);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nWiFi connected, IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  WiFiClient client = server.available();
  while (client) {
    mpu6050.update();
    client.print(mpu6050.getAngleX());
    client.print(',');
    client.print(mpu6050.getAngleY());
    client.print(',');
    client.print(mpu6050.getAngleZ());
    client.print('\n');
  }
}

```
## 使用arduino的pid库计算电机pwm输出
#### 初始化
```
#include <PID_v1.h>
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, Direction)
```

> `Direction`参数：`DIRECT` 或 `REVERSE`，指的是当输入与目标值出现偏差时，向哪个方向控制

#### pid对象方法：
```
//设置输出范围
myPID.SetOutputLimits(min, max)
//执行计算(循环执行)
myPID.Compute()
//启用pid控制
myPID.SetMode(AUTOMATIC);
//动态调参
myPID.SetTunings(Kp, Ki, Kd);
//采样时间，默认采样时间为200ms，单位ms
myPID.SetSampleTime()
//输出参数
myPID.GetKp()
myPID.GetKi()
myPID.GetKd()
myPID.GetMode()
myPID.GetDirection()
```
#### pid控制代码
```
#include <PID_v1.h>
double DegGoal = 0.0, DegIn, DegOut;
double Degkp = 20.0,Degki = 0.5,Degkd = 1.0;
PID DegPID(&DegIn, &DegOut, &DegGoal, Degkp, Degki, Degkd, DIRECT);
DegPID.SetOutputLimits(-127, 127);
DegPID.SetSampleTime(100);
DegPID.SetMode(AUTOMATIC);
while (true){
  mpu6050.update();
  DegIn = mpu6050.getAngleY();
  DegPID.Compute();
}
```
## 同轴麦轮速度分量计算(当然做个已经用不到了)

![大半夜乱涂乱画](photo_2023-02-26_06-19-33.jpg)

其中x和y为平移速度，w为旋转角速度，d和D为轮子与中心距离。
PID平衡控制的值直接加上去就好。

## PID
![PID流程图](7528d75d2ff7922206c42b53b15c26e.png)

使用速度和角度的串级PID控制。

## 直流电机两轮自平衡小车源码
写了串口调参，由于电机没有编码器使用电机pwm代替速度输入。直立问题不大，不过还是很抖，又不是不能用hhh更多改进等用无刷电机foc控制的
```
#include <MPU6050_tockn.h>
#include <Wire.h>
#include <WiFi.h>
#include <PID_v1.h>

const char *ssid = "BJZQ";
const char *password = "12345678";
MPU6050 mpu6050(Wire);
WiFiServer server(80);

double OutPutA, OutPutB;
//角度环
double DegGoal = 1.5, DegIn, DegOut, Degkp = 50.0,Degki = 1.0,Degkd = 0.5;
PID DegPID(&DegIn, &DegOut, &DegGoal, Degkp, Degki, Degkd, DIRECT);
//转向控制
double DirIn, DirOut, DirGoal = 0.0, Dirkp = 3.0, Dirki = 0.0, Dirkd = 0.3;
PID DirPID(&DirIn, &DirOut, &DirGoal, Dirkp, Dirki, Dirkd, DIRECT);
//速度环
double SpdIn, SpdOut, SpdGoal = 0.0, Spdkp = 0.0001, Spdki = 0.0001, Spdkd = 0.00005;
PID SpdPID(&SpdIn, &SpdOut, &SpdGoal, Spdkp, Spdki, Spdkd, DIRECT);

void setup() {
  pinMode(27, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  digitalWrite(32, HIGH);
  digitalWrite(33, HIGH);
  digitalWrite(25, HIGH);
  digitalWrite(26, HIGH);
  ledcSetup(8, 100, 8);
  ledcAttachPin(27, 8);
  ledcWrite(8, 120);
  ledcSetup(6, 100, 8);
  ledcAttachPin(14, 6);
  ledcWrite(6, 120);
  Serial.begin(115200);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  xTaskCreatePinnedToCore(Task1code, "pid_output", 10000, NULL, 1, NULL,  0);
}

void Task1code( void * parameter) {

  DirPID.SetOutputLimits(-63, 63);
  DirPID.SetSampleTime(20);
  DirPID.SetMode(AUTOMATIC);

  DegPID.SetOutputLimits(-127, 127);
  DegPID.SetSampleTime(20);
  DegPID.SetMode(AUTOMATIC);

  SpdPID.SetOutputLimits(-1, 1);
  SpdPID.SetSampleTime(15);
  SpdPID.SetMode(AUTOMATIC);
  
  while (true){
    mpu6050.update();
    DegIn = mpu6050.getAngleY();
    DirIn = mpu6050.getAngleZ();
    DegPID.Compute();
    DirPID.Compute();
    if (DegOut<100&&DegOut>-100){
      DegGoal = DegGoal - SpdOut;
      SpdIn = DegOut;
      SpdPID.Compute();
    }
    OutPutA = DegOut - DirOut;
    OutPutB = DegOut + DirOut;
    if (OutPutA>=0){
      digitalWrite(32, LOW);
      digitalWrite(33, HIGH);
      ledcWrite(6, OutPutA);
    }else{
      digitalWrite(32, HIGH);
      digitalWrite(33, LOW);
      ledcWrite(6, -OutPutA);
    }
    if (OutPutB>=0){
      digitalWrite(25, LOW);
      digitalWrite(26, HIGH);
      ledcWrite(8, OutPutB);
    }else{
      digitalWrite(25, HIGH);
      digitalWrite(26, LOW);
      ledcWrite(8, -OutPutB);
    }
  }
}


void loop() {
  mpu6050.update();
  Serial.print(mpu6050.getAngleX());
  Serial.print(',');
  Serial.print(mpu6050.getAngleY());
  Serial.print(',');
  Serial.print(mpu6050.getAngleZ());
  Serial.print(',');
  Serial.print(DegOut);
  Serial.print(',');
  Serial.print(DegGoal);
  Serial.print(',');
  Serial.print(Degkp);
  Serial.print(',');
  Serial.print(Degki);
  Serial.print(',');
  Serial.print(Degkd);
  Serial.print('\n');
  if (Serial.available()){
    char c = Serial.read();
    if (c=='p'){
      String readBuff;
      unsigned long start_time = millis();
      while(true){
        char c = Serial.read();
        if (c=='\n'||millis()-start_time>100)break;
        readBuff += c;
      }
      Degkp = readBuff.toDouble();
      readBuff = "";
    }
    if (c=='i'){
      String readBuff;
      unsigned long start_time = millis();
      while(true){
        char c = Serial.read();
        if (c=='\n'||millis()-start_time>100)break;
        readBuff += c;
      }
      Degki = readBuff.toDouble();
      readBuff = "";
    }
    if (c=='d'){
      String readBuff;
      unsigned long start_time = millis();
      while(true){
        char c = Serial.read();
        if (c=='\n'||millis()-start_time>100)break;
        readBuff += c;
      }
      Degkd = readBuff.toDouble();
      readBuff = "";
    }
    DegPID.SetTunings(Degkp,Degki,Degkd);
    if (c=='D'){
      String readBuff;
      unsigned long start_time = millis();
      while(true){
        char c = Serial.read();
        if (c=='\n'||millis()-start_time>100)break;
        readBuff += c;
      }
      DirGoal = readBuff.toDouble();
      readBuff = "";
    }
  }
}

```