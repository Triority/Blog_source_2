---
title: 串口调参库
tags:
  - arduino
  - C语言
  - 文档
cover: /img/QQ截图20231204230308.png
categories:
- [折腾记录]
- [文档&笔记]
date: 2023-12-04 22:42:41
description: Adjust the parameters through the serial port
---

# 需求
给DCP调节时序需要频繁修改大量参数，每次参数修改都重新烧录太麻烦了于是有了这个小工具便于串口调参

[github repositories](https://github.com/Triority/Serial_parameter)

# 配置
+ 首先在arduino工程的目录下放置库文件：
[`ser_par.h`](ser_par.h):
```cpp
#include "Arduino.h"
void ser_par(int *par_list[]);
```
[`ser_par.cpp`](ser_par.cpp):
```cpp
#include "Arduino.h"
#include "ser_par.h"

String inString="";
int rec_state = 0;
char rec_char;
int StrtoInt;
int loc_list;

void ser_par(int *par_list[]){
  if(Serial.available()>0){
    if(rec_state==0){
      rec_char = char(Serial.read());
      if(rec_char == 'S'){
        rec_state = 1;
      }
    }
  }

  if(Serial.available()>0){
    if(rec_state==1){
      rec_char = char(Serial.read());
      if (rec_char == 'T'){
        loc_list = inString.toInt();
        rec_state = 2;
        inString="";
      }else{
        inString += rec_char;
      }
    }
  }

  if(Serial.available()>0){
    if(rec_state==2){
      rec_char = Serial.read();
      if (rec_char == '\n'){
        StrtoInt = inString.toInt();
        *par_list[loc_list] = StrtoInt;
        rec_state = 0;
        inString="";
      }else{
        inString += char(rec_char);
      }
    }
  }
}

```

+ 然后就可以在ino主程序引入：`#include "ser_par.h"`

+ 定义一个数组包含你要修改的变量的地址

+ 在loop函数中调用`ser_par()`并传入数组参数

# 使用
串口输入：
```
SaTb\n
```
其中的`S``T``\n`作为标志字符不可修改，`a`代表你要修改的参数在数组的索引，`b`代表设置成的值，`\n`为换行符，arduino串口发送可配置是否发送换行符（默认发送）

# 示例
[`Serial_parameter.ino`](Serial_parameter.ino):
```cpp
#include "ser_par.h"

int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;

int *par_list[5] = {&a,&b,&c,&d,&e};

void setup() {
  Serial.begin(115200);
}

void loop() {
  //do something
  delay(100);

  //Serial_parameter function
  ser_par(par_list);

  //print results
  Serial.printf("a:%d, b:%d, c:%d, d:%d, e:%d\n",a,b,c,d,e);
}

```
