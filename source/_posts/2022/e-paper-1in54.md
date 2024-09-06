---
title: 1.54寸双色墨水屏arduino及树莓派驱动
date: 2022-08-07 18:55:38
tags:
- arduino
- python
- 显示屏
description: 一个1.54寸双色墨水屏的折腾日记
cover: /img/e-paper-1in54.png
categories: 
- 折腾记录
---
# 前言
前几日逛淘宝发现一个1.54寸双色墨水屏，屏幕+驱动只要16，果断下单拿来玩玩
[第二天就涨价到了26了hhhhhhhhhhhc]
如果还有人感兴趣的话在这：[某宝链接](https://m.tb.cn/h.fA3mNRx?tk=MW9n2sLzRZj "某宝链接")
# arduino
## 接线
在[微雪官网资料](https://www.waveshare.net/wiki/1.54inch_e-Paper_Module_Manual "微雪官网资料")找到接线图：
![接线图](接线图.png)
虽然和我的引脚名称不太一样，但是不影响理解和使用。
## 程序
当然也是在微雪官网下载的资料，注释都是英文而且一些有点问题，这里整理一下
[微雪资料下载链接](https://www.waveshare.net/w/upload/3/39/E-Paper_code.7z "微雪资料下载链接")
由于我的屏幕是1.54寸，所以在`arduino`的`epd1in54`文件夹内
主要需要改动的是`epd1in54.ino`和`imagedata.cpp`
#### imagedata.cpp
这个文件要修改的是那个保存图片的数组。图片转换数组可以用微雪提供的工具：[图片取模软件](https://www.waveshare.net/w/upload/3/36/Image2Lcd.7z "图片取模软件")
打开后是这样：
![取模软件](image2lcd.png)
首先修改图片尺寸，我的屏幕是200x200.
然后左上角打开，选择一张图片，修改参数后保存为c语言数组。
打开保存的数组文件可以看见：
![数组文件](数组文件.png)
用数组数据替换掉原来文件里的数据
需要注意的是复制的时候跳过数组第一行，从第二行开始复制，否则最后显示的图片会发生偏移
#### epd1in54.ino
废话不多说直接上代码和注释：
```cpp
#include <SPI.h>
#include "epd1in54.h"
#include "epdpaint.h"
#include "imagedata.h"
#define COLORED     0
#define UNCOLORED   1
//初始化图片缓存，由于一个字节8个像素点，所以这里必须是8的倍数
unsigned char image[1024];
Paint paint(image, 0, 0);
//墨水屏实例化
Epd epd;
void setup() {
  Serial.begin(115200);
  Serial.print("e-Paper init ");
  //全刷初始化
  if (epd.Init(lut_full_update) != 0) {
      Serial.print("e-Paper init failed");
      return;
  }
  //清屏两次
  //电子纸显示屏中嵌入了2个存储区域，一旦刷新显示，内存区域将自动切换，即 SetFrameMemory 的下一个操作将设置其他内存区域，因此，您必须清除帧内存两次。
  epd.ClearFrameMemory(0xFF);
  epd.DisplayFrame();
  epd.ClearFrameMemory(0xFF); 
  epd.DisplayFrame();
  //设置paint翻转角度，宽，高
  paint.SetRotate(ROTATE_0);
  paint.SetWidth(200);
  paint.SetHeight(24);
  //将paint设置为黑色，在paint的（30,4）这一点为左顶点写字符串，字体大小为16，颜色为白色,并将paint写入到图片中
  paint.Clear(COLORED);
  paint.DrawStringAt(30, 4, "Hello world!", &Font16, UNCOLORED);
  epd.SetFrameMemory(paint.GetImage(), 0, 10, paint.GetWidth(), paint.GetHeight());
  //将paint设置为黑色，在paint的（0,2）这一点为左顶点写字符串，字体大小为24，颜色为黑色,并将paint写入到图片中
  paint.Clear(UNCOLORED);
  paint.DrawStringAt(0, 2, "e-Paper Demo", &Font24, COLORED);
  epd.SetFrameMemory(paint.GetImage(), 0, 30, paint.GetWidth(), paint.GetHeight());
  //重新设置paint的宽高
  paint.SetWidth(64);
  paint.SetHeight(64);
  //画3条线并写入图片
  paint.Clear(UNCOLORED);
  paint.DrawRectangle(0, 0, 40, 50, COLORED);
  paint.DrawLine(0, 0, 40, 50, COLORED);
  paint.DrawLine(40, 0, 0, 50, COLORED);
  epd.SetFrameMemory(paint.GetImage(), 16, 60, paint.GetWidth(), paint.GetHeight());
  //打开显示
  epd.DisplayFrame();
  delay(8000);
  //刷新显示两次原图。
  epd.SetFrameMemory(IMAGE_DATA);
  epd.DisplayFrame();
  epd.SetFrameMemory(IMAGE_DATA);
  epd.DisplayFrame();
  //睡眠
  epd.Sleep();
}
void loop() {
}
```
这里我删掉了原来资料的画图部分，只保留了字符串显示，画图直接看[微雪文档](https://www.waveshare.net/wiki/1.54inch_e-Paper_Module_Manual#.E4.B8.8A.E5.B1.82.E5.BA.94.E7.94.A8_4 "微雪文档")就好
但是还有一个问题，资料中没有关于局部刷新的demo，只在文档里提到了局部刷新的初始化方式。这里暂时留坑。
# 树莓派