---
title: arduino寻线小车
date: 2022-07-11 16:36:14
tags:
- arduino
- C语言
description: 之前浅学了一下做巡线车，代码很烂仅供参考
cover: /img/arduino_line_follower.jpg
categories: 
- 折腾记录
---
```c
//引脚定义
int Left_motor=8;     //左电机(IN3) 输出0  前进   输出1 后退
int Left_motor_pwm=9;     //左电机PWM调速
int Right_motor_pwm=10;    // 右电机PWM调速
int Right_motor=11;    // 右电机
const int Middle = 13;    //中传感器(P3.2 OUT1)
const int Left1 = 4;      //左1传感器(P3.3 OUT2)
const int Right1 = 6;     //右1传感器(P3.2 OUT1)
const int Left2 = 12;     //左2传感器(P3.3 OUT2)
const int Right2 = 2;     //右2传感器(P3.2 OUT1)
const int Left3 = 3;      //左中断传感器(P3.3 OUT2)
const int Right3 = 5;     //右中断传感器(P3.2 OUT1)
int beep=A3;//定义蜂鸣器
//传感器状态定义,计数,中断定义
int M,L1,R1,L2,R2,L3,R3;
int go=0;   //行进状态
int t = 10;//超时判断
int t1 = 0;//左转判断
int t2 = 0;//右转判断
//初始化
void setup(){
  Serial.begin(9600);
  pinMode(Left_motor,OUTPUT); // PIN 8 8脚无PWM功能
  pinMode(Left_motor_pwm,OUTPUT); // PIN 9 (PWM)
  pinMode(Right_motor_pwm,OUTPUT);// PIN 10 (PWM) 
  pinMode(Right_motor,OUTPUT);// PIN 11 (PWM)
  pinMode(Middle, INPUT);
  pinMode(Left1, INPUT);
  pinMode(Right1, INPUT);
  pinMode(Left2, INPUT);
  pinMode(Right2, INPUT);
  pinMode(Left3, INPUT);
  pinMode(Right3, INPUT);
  pinMode(beep,OUTPUT);
}
//电机输出
void a(){
  digitalWrite(Left_motor,LOW);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,110);//PWM比例0~255调速，左右轮差异略增减 
  digitalWrite(Right_motor,LOW);  // 右电机前进
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,110);//PWM比例0~255调速，左右轮差异略增减
}
void left(){
  digitalWrite(Left_motor,HIGH);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,5);//PWM比例0~255调速，左右轮差异略增减  
  digitalWrite(Right_motor,LOW);  // 右电机前进
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,130);//PWM比例0~255调速，左右轮差异略增减
}
void left2(){
  digitalWrite(Left_motor,HIGH);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,20);//PWM比例0~255调速，左右轮差异略增减  
  digitalWrite(Right_motor,LOW);  // 右电机前进
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,160);//PWM比例0~255调速，左右轮差异略增减
}
void turnleft(){
  digitalWrite(Left_motor,HIGH);  // 左电机后退
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,150);//PWM比例0~255调速，左右轮差异略增减
  digitalWrite(Right_motor,LOW);  // 右电机前进
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,120);//PWM比例0~255调速，左右轮差异略增减
}
void right(){
  digitalWrite(Left_motor,LOW);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,130);//PWM比例0~255调速，左右轮差异略增减 
  digitalWrite(Right_motor,HIGH);  // 右电机不转
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机PWM输出0     
  analogWrite(Right_motor_pwm,5);//PWM比例0~255调速，左右轮差异略增减
}
void right2(){
  digitalWrite(Left_motor,LOW);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,160);//PWM比例0~255调速，左右轮差异略增减 
  digitalWrite(Right_motor,HIGH);  // 右电机不转
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机PWM输出0     
  analogWrite(Right_motor_pwm,20);//PWM比例0~255调速，左右轮差异略增减
}
void turnright(){
  digitalWrite(Left_motor,LOW);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,120);//PWM比例0~255调速，左右轮差异略增减
  digitalWrite(Right_motor,HIGH);  // 右电机后退
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机PWM输出1     
  analogWrite(Right_motor_pwm,150);//PWM比例0~255调速，左右轮差异略增减
}
void Beep(){
digitalWrite(beep,HIGH);
delay(50);
digitalWrite(beep,LOW);
}
//循环
void loop(){
//黑线为HIGH
  M = digitalRead(Middle);
  L1 = digitalRead(Left1);
  R1 = digitalRead(Right1);
  L2 = digitalRead(Left2);
  R2 = digitalRead(Right2);
  L3 = digitalRead(Left3);
  R3 = digitalRead(Right3);
//计时=======================================
if(M==HIGH||L1==HIGH||R1==HIGH){t=3;}
if(L2==HIGH||R2==HIGH){t=3;}
if(L3==HIGH){t1=0;}
if(R3==HIGH){t2=0;}
//电机输出
if (M == HIGH || (L1 == HIGH && R1 == HIGH)){go=1;}else
if (L1 == HIGH){go=2;}else
if (R1 == HIGH){go=3;}else
if (L2 == HIGH){go=4;}else
if (R2 == HIGH){go=5;}
if(t<0){
  if(t1>t2&&t2<=100){
    go=7;
    }
  if(t1<t2&&t1<=100){
    go=6;
    }
  }

if(go==1){
    a();}
  else if (go==2){
    left();}
  else if (go==3){
    right();}
  else if (go==4){
    left2();}
  else if (go==5){
    right2();}
    else if (go==6){
    turnleft();}
  else if (go==7){
    turnright();}

  t1=t1+1;
  t2=t2+1;
  t=t-1;

  Serial.print("  t  ");
  Serial.print(t);
  Serial.print("  t1  ");
  Serial.print(t1);
  Serial.print("  t2  ");
  Serial.print(t2);
  Serial.print("  go  ");
  Serial.print(go);
  Serial.print("\n");
}
```