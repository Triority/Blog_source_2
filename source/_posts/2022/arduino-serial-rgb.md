---
title: arduino中解析串口字符串
description: 很久很久以前我想做arduino从蓝牙串口接受手机信息调节RGB灯颜色,但是由于字符串处理的困难被迫放弃,上次写了arduino串口函数的文章,有了新的思路...
cover: /img/arduino-serial-rgb.png
date: 2022-05-15 12:24:04
categories: 
- 折腾记录
tags:
- arduino
---
## 串口通信传输RGB数值

很久很久以前我想做arduino从蓝牙串口接受手机信息调节RGB灯颜色,但是由于字符串处理的困难被迫放弃,上次写了arduino串口函数的文章,有了新的思路...

数据格式:R100G200B255X, 其中X为终止标识

[下载手机APP连接蓝牙并发送RGB数值](base.apk "APP")

RGB引脚为9,10,11,串口引脚5(蓝牙TXD),6(蓝牙RXD)

循环读取每一个字符存储在rec
如果读取'R'则将后面的字符存储进R字符串,GB同理
这里还有个奇怪的问题就是如果没有delay(5);得到的R字符串就会在首位多一个乱码符号，之所以奇怪，是因为G和B不影响，但出于代码的美观和稳定性我还是都加上了delay(5);语句
刚开始存储RGB的字符串直接使用atoi()函数转换成数字,但是出现了错误,因为需要先转换成const char*类型,所以改为atoi(R.c_str());

```c
#include <SoftwareSerial.h>
String rec="",R="",G="",B="";
char r,g,b;
int rr,gg,bb;
SoftwareSerial BT(5, 6);
void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(9,OUTPUT); // PIN 9 (PWM)
  pinMode(10,OUTPUT);// PIN 10 (PWM) 
  pinMode(11,OUTPUT);// PIN 11 (PWM)
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
}

void loop() {
  rec = "";
  while (BT.available() > 0){
    rec = char(BT.read());
    Serial.println(rec);
    if (rec=="R"){
      Serial.println("receved R");
      delay(5);
      rec = char(BT.read());
      r = true;
      g = false;
      b = false;
    }
    if (rec=="G"){
      Serial.println("receved G");
      delay(5);
      rec = char(BT.read());
      r = false;
      g = true;
      b = false;
    }
    if (rec=="B"){
      Serial.println("receved B");
      delay(5);
      rec = char(BT.read());
      r = false;
      g = false;
      b = true;
    }
    if (rec=="X"){
      Serial.println("finished");
      r = false;
      g = false;
      b = false;
      rr = atoi(R.c_str());
      gg = atoi(G.c_str());
      bb = atoi(B.c_str());
      Serial.println(rr);
      Serial.println(gg);
      Serial.println(bb);
      R = "";
      G = "";
      B = "";
      analogWrite(9,rr);
      analogWrite(10,gg);
      analogWrite(11,bb);
    }
    if (r==true)R+=rec;
    if (g==true)G+=rec;
    if (b==true)B+=rec;
    delay(10);
  }
}

```