---
title: tft-espi使用sprite方法实现动画效果
tags:
  - arduino
  - 显示屏
  - esp32
cover: /img/微信截图_20230720023001.png
categories:
- 折腾记录
date: 2023-07-03 01:59:19
description: 这个其实是为了实现早就想做的蓝牙小键盘的前置任务，也就是配合旋钮的动画效果
---
# 功能目标
实现在彩色tft屏幕上做一个字符移动的动画效果，之前尝试过用u8g2库但是传输速度超级慢，每帧要好几秒那种，完全不能用，这次尝试了使用tft_espi库，真香hhh
# TFT_ESPI
点亮tft屏幕这一部分可以参考学弟写的[ESP32使用TFT屏幕全踩坑指南](https://qwqpap.xyz/esp32%e4%bd%bf%e7%94%a8tft%e5%b1%8f%e5%b9%95%e5%85%a8%e8%b8%a9%e5%9d%91%e6%8c%87%e5%8d%97/330.html)

# tft.fillScreen
首先尝试了一下使用全屏重写的方法实现字符动画效果
```
#include <SPI.h>

#include <TFT_eSPI.h>       // Hardware-specific library

TFT_eSPI tft = TFT_eSPI();  // Invoke custom library

void setup(void) {
  
  tft.init();

  tft.fillScreen(TFT_BLACK);
}

void show(int x){
  tft.invertDisplay( false ); // Where i is true or false
 
  tft.fillScreen(TFT_BLACK);

  tft.setCursor(x, 120, 4);

  tft.setTextColor(TFT_WHITE);
  tft.println("Hello World");
}

void loop() {
  int x = 0;
  while (x<200){
  show(x);
  x += 2;
  }

  while (x>0){
  show(x);
  x -= 3;
  }
}
```
尝试后问题十分明显，由于全屏刷新屏幕一直在闪烁，虽然也可以换用局部刷新的方法，但是依然非常不优雅

# Sprite尝试
## 例程
首先是一个tft_espi的例程
```
// Set delay after plotting the sprite
#define DELAY 1000

// Width and height of sprite
#define WIDTH  128
#define HEIGHT 128

#include <TFT_eSPI.h>                 // Include the graphics library (this includes the sprite functions)

TFT_eSPI    tft = TFT_eSPI();         // Declare object "tft"

TFT_eSprite spr = TFT_eSprite(&tft);  // Declare Sprite object "spr" with pointer to "tft" object

void setup()
{
  Serial.begin(250000);
  Serial.println();

  // Initialise the TFT registers
  tft.init();

  // Optionally set colour depth to 8 or 16 bits, default is 16 if not specified
  // spr.setColorDepth(8);

  // Create a sprite of defined size
  spr.createSprite(WIDTH, HEIGHT);

  // Clear the TFT screen to blue
  tft.fillScreen(TFT_BLUE);
}

void loop(void)
{
  // Fill the whole sprite with black (Sprite is in memory so not visible yet)
  spr.fillSprite(TFT_BLACK);

  // Number of pixels to draw
  uint16_t n = 100;

  // Draw 100 random colour pixels at random positions in sprite
  while (n--)
  {
    uint16_t colour = random(0x10000); // Returns colour 0 - 0xFFFF
    int16_t x = random(WIDTH);        // Random x coordinate
    int16_t y = random(HEIGHT);       // Random y coordinate
    spr.drawPixel( x, y, colour);      // Draw pixel in sprite
  }

  // Draw some lines
  spr.drawLine(1, 0, WIDTH, HEIGHT-1, TFT_GREEN);
  spr.drawLine(0, 0, WIDTH, HEIGHT, TFT_GREEN);
  spr.drawLine(0, 1, WIDTH-1, HEIGHT, TFT_GREEN);
  spr.drawLine(0, HEIGHT-1, WIDTH-1, 0, TFT_RED);
  spr.drawLine(0, HEIGHT, WIDTH, 0, TFT_RED);
  spr.drawLine(1, HEIGHT, WIDTH, 1, TFT_RED);

  // Draw some text with Middle Centre datum
  spr.setTextDatum(MC_DATUM);
  spr.drawString("Sprite", WIDTH / 2, HEIGHT / 2, 4);

  // Now push the sprite to the TFT at position 0,0 on screen
  spr.pushSprite(-40, -40);
  spr.pushSprite(tft.width() / 2 - WIDTH / 2, tft.height() / 2 - HEIGHT / 2);
  spr.pushSprite(tft.width() - WIDTH + 40, tft.height() - HEIGHT + 40);

  delay(DELAY);

  // Fill TFT screen with blue
  tft.fillScreen(TFT_BLUE);

  // Draw a blue rectangle in sprite so when we move it 1 pixel it does not leave a trail
  // on the blue screen background
  spr.drawRect(0, 0, WIDTH, HEIGHT, TFT_BLUE);

  int x = tft.width() / 2  -  WIDTH / 2;
  int y = tft.height() / 2 - HEIGHT / 2;

  uint32_t updateTime = 0;       // time for next update

  while (true)
  {
    // Random movement direction
    int dx = 1; if (random(2)) dx = -1;
    int dy = 1; if (random(2)) dy = -1;

    // Pull it back onto screen if it wanders off
    if (x < -WIDTH/2) dx = 1;
    if (x >= tft.width()-WIDTH/2) dx = -1;
    if (y < -HEIGHT/2) dy = 1;
    if (y >= tft.height()-HEIGHT/2) dy = -1;

    // Draw it 50 time, moving in random direct or staying still
    n = 50;
    int wait = random (50);
    while (n)
    {
      if (updateTime <= millis())
      {
        // Use time delay so sprite does not move fast when not all on screen
        updateTime = millis() + wait;

        // Push the sprite to the TFT screen
        spr.pushSprite(x, y);

        // Change coord for next loop
        x += dx;
        y += dy;
        n--;
        yield(); // Stop watchdog reset
      }
    }
  } // Infinite while, will not exit!
}
```
可以看到中间那个图案四处移动非常丝滑，简直完美解决方案

## 分析
这里我就把原例程稍作修改，只保留必要部分以便于理解，顺便把注释翻译为中文了

(sprite不知道应该怎么翻译，就写英文了。现在是七月初北京天天40度真想翻译成雪碧hhh)
```
// 设置绘制sprite之后的延迟时间
#define DELAY 500
// 设置sprite的宽高
#define WIDTH  120
#define HEIGHT 120

#include <TFT_eSPI.h>
TFT_eSPI    tft = TFT_eSPI();
TFT_eSprite spr = TFT_eSprite(&tft);  // 声明带有 "tft" 指针对象的 Sprite 对象 "spr" 

void setup(){
  tft.init();
  // 可将颜色深度设置为 8 或 16 位，如果未指定，则默认值为 16
  // spr.setColorDepth(8);
  // 创建一个sprite
  spr.createSprite(WIDTH, HEIGHT);

  tft.fillScreen(TFT_BLUE);
}

void loop(void)
{
  // 填充整个sprite为黑色 (Sprite 还在内存中所以不可见)
  spr.fillSprite(TFT_BLACK);

  // 在sprite里画几条线
  spr.drawLine(1, 0, WIDTH, HEIGHT-1, TFT_GREEN);
  spr.drawLine(0, 0, WIDTH, HEIGHT, TFT_GREEN);
  spr.drawLine(0, 1, WIDTH-1, HEIGHT, TFT_GREEN);
  spr.drawLine(0, HEIGHT-1, WIDTH-1, 0, TFT_RED);
  spr.drawLine(0, HEIGHT, WIDTH, 0, TFT_RED);
  spr.drawLine(1, HEIGHT, WIDTH, 1, TFT_RED);
  // 在中间写一些字
  spr.setTextDatum(MC_DATUM);
  spr.drawString("Sprite", WIDTH / 2, HEIGHT / 2, 4);

  // 将Sprite显示在屏幕中间
  spr.pushSprite(-40, -40);
  spr.pushSprite(tft.width() / 2 - WIDTH / 2, tft.height() / 2 - HEIGHT / 2);
  spr.pushSprite(tft.width() - WIDTH + 40, tft.height() - HEIGHT + 40);

  delay(DELAY);

  // 填充TFT屏幕为蓝色
  tft.fillScreen(TFT_BLUE);

  // 在Sprite中绘制一个蓝色矩形，这样当我们将他移动 1 个像素时不会在蓝色背景留下痕迹
  spr.drawRect(0, 0, WIDTH, HEIGHT, TFT_BLUE);

  int x = tft.width() / 2  -  WIDTH / 2;
  int y = tft.height() / 2 - HEIGHT / 2;

  while (true)
  {
    // 随机移动方向
    int dx = 1; if (random(2)) dx = -1;
    int dy = 1; if (random(2)) dy = -1;

    // 如果移动离开了屏幕就拉回来
    if (x < -WIDTH/2) dx = 1;
    if (x >= tft.width()-WIDTH/2) dx = -1;
    if (y < -HEIGHT/2) dy = 1;
    if (y >= tft.height()-HEIGHT/2) dy = -1;

    // 随机移动绘制50次
    int n = 50;
    while (n){
      //delay(10);
      // 将Sprite显示在屏幕上并设置下次显示位置
      spr.pushSprite(x, y);
      x += dx;
      y += dy;
      n--;
      //yield(); // 停止看门狗复位（不知道干嘛用而且删掉了没有影响）
    }
  }
}
```
看完注释的内容差不多也就基本会用sprite这个神奇的东西了，可以做下一步工作了

简单尝试一下做个根据电位器移动的字符串

电位器是连接在VP引脚上的，也就是GPIO39，屏幕接线不变

里面有一些魔法数字，是适配我这个240*240的屏幕的，如果是其他分辨率的屏幕可能需要做些修改

```
// 设置sprite的宽高
#define WIDTH  120
#define HEIGHT 120
#include <TFT_eSPI.h>
TFT_eSPI    tft = TFT_eSPI();
TFT_eSprite spr = TFT_eSprite(&tft);

void setup(){
  Serial.begin(115200);
  tft.init();
  spr.setColorDepth(8);
  // 创建一个sprite
  spr.createSprite(WIDTH, HEIGHT);

  tft.fillScreen(TFT_BLACK);
}

void loop(void){
  // 填充整个sprite为黑色 (Sprite 还在内存中所以不可见)
  spr.fillSprite(TFT_BLACK);

  spr.setTextDatum(MC_DATUM);
  spr.drawString("Sprite", WIDTH/2, HEIGHT/2, 4);
  spr.pushSprite(tft.width()/2 - WIDTH/2, tft.height()/2 - HEIGHT/2);

  tft.fillScreen(TFT_BLACK);

  int x = tft.width() / 2  -  WIDTH / 2;
  int y = tft.height() / 2 - HEIGHT / 2;
  while (true){
  int analogValueX=analogReadMilliVolts(39);
  int x_goal = analogValueX*240/3300;

  x+=(x_goal-x)/10;

  spr.pushSprite(x-60, 60);
  }
}
```

效果很棒，非常丝滑舒适
{% dplayer "url=edcc5dd7253720d2441f86f45a76d544.mp4" %}
# Sprite方法
