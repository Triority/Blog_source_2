---
title: 树莓派拍摄3D打印延时摄影[顺便写了个arduino电压表]
description: 年初DIY的3D打印机使用12V电源电压,而拍摄延时摄影的树莓派使用5V电压,所以三月份买了一个12v转5v的降压模块,但是为了保证安全,想用电压表测量一下降压模块的输出电压,于是...
cover: /img/arduino-voltmeter.jpg
date: 2022-05-17 19:32:00
categories: 
- 折腾记录
tags:
- arduino
- 3D打印
- 显示屏
- 树莓派
---
## arduino电压表
### 小故事
年初DIY的3D打印机使用12V电源电压,而拍摄延时摄影的树莓派使用5V电压,所以三月份买了一个12v转5v的降压模块[因为沈阳疫情我们小区封控两个多月...所以才到],但是为了保证安全,想用电压表测量一下降压模块的输出电压,于是使用arduino的模拟输入接口来测量0-5V电压,为了提高量程,在淘宝risym旗舰店买了一个电压传感器模块,可以将电压降低5倍,也就是量程提高到0-25V.
arduino使用除法时会自动删去小数位,所以用了求余的方法求小数位,并将计算的电压结果通过串口传输给电脑以及显示在OLED屏幕
### arduino程序

```c
#include "U8glib.h"
#include <string.h>

U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NONE|U8G_I2C_OPT_DEV_0);	// I2C / TWI 

int val=0;
int val0;
int val1;
char str1[2];
char str2[2];
char str3[2]=".";

void draw(void) {
  // graphic commands to redraw the complete screen should be placed here  
  u8g.setFont(u8g_font_unifont);
  //u8g.setFont(u8g_font_osb21);
  char str[20]="v=";
  val = analogRead(0)*25;
  Serial.println(val); 
  val0 = val/1024;
  Serial.println(val0); 
  val1 = (val%1024)*10/1024;
  Serial.println(val1); 
  itoa(val0, str1, 10);
  itoa(val1, str2, 10);
  strcat(str,str1);
  strcat(str,str3);
  strcat(str,str2);
  u8g.drawStr( 10, 35, str);
}

void setup(void) {
  Serial.begin(9600);
  // flip screen, if required
  // u8g.setRot180();
  
  // set SPI backup if required
  //u8g.setHardwareBackup(u8g_backup_avr_spi);

  // assign default color value
  if ( u8g.getMode() == U8G_MODE_R3G3B2 ) {
    u8g.setColorIndex(255);     // white
  }
  else if ( u8g.getMode() == U8G_MODE_GRAY2BIT ) {
    u8g.setColorIndex(3);         // max intensity
  }
  else if ( u8g.getMode() == U8G_MODE_BW ) {
    u8g.setColorIndex(1);         // pixel on
  }
  else if ( u8g.getMode() == U8G_MODE_HICOLOR ) {
    u8g.setHiColorByRGB(255,255,255);
  }
}

void loop(void) {
  // picture loop
  u8g.firstPage();  
  do {
    draw();
  } while( u8g.nextPage() );
  
  // rebuild the picture after some delay
  delay(200);
}
```
### 测量结果
测量得知电压在5.0-5.4之间浮动,多数时间稳定在5.1V,可以给树莓派供电.

{% asset_img arduino-voltmeter.jpg 测量照片 %}

## 树莓派拍摄3D打印延时摄影
### 每层拍照
使用限位开关检测打印头是否回到原点.若回到原点则触发拍照,得到每一层时候的照片

```python
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
i=1
j=1
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print ("begin..")
while False and not GPIO.input(11):
    time.sleep(1)
    print ("heating..."+str(j))
    j=j+1
camera = PiCamera()
camera.start_preview()
print ("start")
while True:
    if not GPIO.input(11):
        print(i)
        camera.capture('/home/pi/Desktop/cam_3D/cam_3D/image%s.jpg' % i)
        i=i+1
        time.sleep(5)
    time.sleep(1)
```
### 每层照片合成视频
这一步建议电脑上完成否则可能要运行一段时间
记得把size改成实际照片的尺寸,另外如果照片个数多于1000也要增加for循环的次数.
```python
import numpy as np
import cv2
size = (1024,768)
videowrite = cv2.VideoWriter(r'test.mp4',-1,30,size)
img_array=[]
for filename in [r'cam_3D\image{0}.jpg'.format(i) for i in range(1,1000)]:
    img = cv2.imread(filename)
    if img is None:
        print(filename + " is error!")
        continue
    img_array.append(img)
for i in range(1000):
    videowrite.write(img_array[i])
videowrite.release()
print('finished')
```