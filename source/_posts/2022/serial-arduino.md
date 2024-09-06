---
title: Arduino笔记:serial相关操作
description: 记录了Arduino串口通讯相关的函数
cover: /img/arduino.png
date: 2022-05-09 22:04:53
categories: 
- 文档&笔记
tags:
- arduino
- 笔记
---
## Stream 类函数
**Stream 的这些函数 都会被 Serial 库继承。**

####  available()
说明（Description）: 获取数据流中接收到的字节数
返回值（Returns）：返回值是 int 类型

#### read()
说明（Description）：获取数据流中第一个字节数据，获取数据后会清除当前字节数据，与peek()函数有区别
返回值（Returns）：读取数据字符的第一个字节（8bit）

#### flush()
说明（Description）：清除数据流所有未向外发送的数据。
返回值（Returns）：bool 类型

#### find()
说明（Description）：从数据流中查找目标字符串，找到目标字符串后返回值 = true，超时则返回值 = false
返回值（Returns）：bool 类型

####  findUntil()
说明（Description）：从数据流中读取目标字符串或者终止目标字符串，找到目标字符串后返回值 = true，超时则返回值 = false
语法（Syntax）：
　　stream.findUntil(target, terminal)
　　target：要搜索的字符串
　　terminal：终止目标字符串
返回值（Returns）：bool 类型

####  peek()
说明（Description）：从数据流中读取当前的一个字节，不会清除数据流中当前字节数据，与 read() 函数有区别。
返回值（Returns）：当前缓存区数据流的第一个字节数据，如果缓存区无数据时返回 -1

#### readBytes()
说明（Description）：) 从数据流中读取确定字节的数据到缓存区，读取确定长度数据或超时时终止
语法（Syntax）：
　　stream.readBytes(buffer, length)
　　stream：从 Stream 类 继承的实例
　　buffer：存放数据的缓存区（可以是 char[] 或 byte[] 这样的数组）
　　length：存放的字节数
返回值（Returns）：已经存放在缓存区中的字节数

#### readBytesUntil()
说明（Description）：从数据流中读取确定字节的数据到指定缓存地址，读取确定长度数据、或读取到终止字符、或超时时终止. 和 readBytes() 相比多了终止字符串
语法（Syntax）：
　　stream.readBytesUntil(character, buffer, length)
　　stream：从 Stream 类 继承的实例
　　character：终止字符（char 类型）
　　buffer：存放数据的指定缓存地址（可以是 char[] 或 byte[] 这样的数组）
　　length：存放的字节数（int 类型）
返回值（Returns）：已经存放在缓存区中的字节数

#### readString()
说明（Description）：从数据流中读取字符到字符串中，超时时终止
返回值（Returns）：读取到的字符串（string）

#### readStringUntil()
说明（Description）：从数据流中读取字符到字符串中，遇到终止字符，或超时时终止
语法（Syntax）：
　　stream.readString(terminator)
　　terminator：终止字符
返回值（Returns）：读取到的字符串（string）

#### parseInt()
说明（Description）：从数据流中读取第一个 长整型数（long），
返回值（Returns）：长整型（long）

#### parseFloat()
说明（Description）：从数据流中读取第一个有效的浮点数（float），
语法（Syntax）：
　　stream.parseFloat(list)
　　list：检查的数据流
返回值（Returns）：浮点数（float）

#### setTimeout()
说明（Description）：设置等待数据流通讯超时时间，毫秒为单位
语法（Syntax）：
　　stream.setTimeout(time)
　　time：毫秒为单位的时间，长整型（long）

## Serial 类
Serial 继承 Stream 类，继承的函数方法参考 Stream 类；同时增加了几个新的函数，所有方法如下：

#### begin()
说明（Description）：设置串口数据传输的波特率。
语法（Syntax）：
　　Serial.begin(speed)
　　Serial.begin(speed, config)
　　speed：波特率 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, or 115200
　　config：通讯格式 5N1, 6N1, 7N1, 8N1(默认), 5N2, 6N2, 7N2, 8N2, 5E1, 6E1, 7E1, 8E1, 5E2, 6E2, 7E2, 8E2, 5O1, 6O1, 7O1, 8O1, 5O2, 6O2, 7O2, 8O2,
返回值（Returns）：nothing 无

#### end()
说明（Description）：禁用串口。禁用串口后，原串口所占用引脚被当做一般输入输出使用。
语法（Syntax）：
　　Serial.end()
返回值（Returns）：nothing 无

#### print()
说明（Description）：将数据流通过串口以 ASCII 文本形式输出输出。
例子：
Serial.print(78) gives "78"　　以 ASCII 码形式以此输出 “7” 和 “8”
Serial.print(1.23456) gives "1.23"　　浮点数默认只输出小数点后两位
Serial.print('N') gives "N"　
Serial.print("Hello world.") gives "Hello world."
Serial.print(78, BIN) gives "1001110"
Serial.print(78, OCT) gives "116"
Serial.print(78, DEC) gives "78"
Serial.print(78, HEX) gives "4E"
Serial.println(1.23456, 0) gives "1"
Serial.println(1.23456, 2) gives "1.23"
Serial.println(1.23456, 4) gives "1.2346"
语法（Syntax）：
　　Serial.print(val)
　　Serial.print(val, format)
　　val：需要输出的值，支持任何类型数据
　　format：指定数据格式
返回值（Returns）：返回 print() 函数输出的字符数据个数，长整型（long）

#### println()
说明（Description）：将数据流通过串口以 ASCII 文本形式输出输出，并且在结尾输出换行符 (ASCII 13, 即 '\r') 。参考 print() 函数
语法（Syntax）：
　　Serial.println(val)
　　Serial.println(val, format)
　　val：需要输出的值，支持任何类型数据
　　format：指定数据格式
返回值（Returns）：输出的字符数据个数，长整型（long）

#### write()
说明（Description）：将数据流通过串口以 二进制数据的形式发出，与 print() 函数是有区别的
语法（Syntax）：
　　Serial.write(val)
　　Serial.write(str)
　　Serial.write(buf, len)
　　val：单个字节的值
　　str：一连串字节的字符串
　　buf：定义的数组
　　len：指定的数组长度
返回值（Returns）：函数通过写入串口的字节数

#### serialEvent()
说明（Description）：串口中断事件函数，当串口有数据时被调用。可使用 Serial.read() 函数捕捉数据。
语法（Syntax）：
　　void serialEvent(){
　　　　//statements
　　　}
statements：任何有效的语句

文章部分转载自[aiyauto的博客](https://www.cnblogs.com/aiyauto/p/7071712.html "aiyauto的博客")