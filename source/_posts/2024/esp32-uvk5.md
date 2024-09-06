---
title: 使用无线电台模拟音频信号传输文本数据
tags:
  - arduino
  - esp32
  - 无线电
cover: /img/fde96b3ea3b995379fadc65a705774e.png
categories:
  - - 折腾记录
  - - 无线电
date: 2024-03-05 19:05:13
description: 用于未来可能的一次神秘小活动
---
# 实现目标
以较低成本实现无线电台传输少量数据

未来可能放一个探空气球，计划应该让氦气球在平流层爆炸并使得负载降落，但是高空没有基站信号，如果等降落到地面之后使用4G信号返回位置数据，有可能降落到基站信号范围之外无法找回，因此使用无线电台就是最佳解决方案。、

同时由于有可能找不回负载设备，所以希望尽量降低负载成本，可以传输数据的电台又过于昂贵因此出此下策：使用模拟手台语音通联，直接esp32产生正弦波音频信号通过手台发送，然后手台接收进行解码得到位置数据。

# 空中发射
## 载波
下面代码可以实现esp32使用dac外设发送500Hz的正弦信号

需要注意的是由于esp32的dac性能限制，信号频率最好不要高于1k，否则失真明显(但是这里我又不需要完美的正弦信号我只要频率所以高一点无所谓了，还留着正弦只是照顾一下电台的模拟电路)

| ![](009.BMP)  | ![](001.BMP)  | ![](005.BMP)  | ![](006.BMP)  |
| :------------: | :------------: | :------------: | :------------: |
| 2000Hz  | 1000Hz  |  500Hz |  250Hz |

```c
hw_timer_t *timer = NULL;

unsigned long angle = 0;
int value;
//设置为100时输出正弦波频率为500hz
int add_value = 100;

//定时器中断函数
void IRAM_ATTR InterruptEvent(){
  angle = angle + add_value;
}

void setup(){
  Serial.begin(115200);
  //定时器初始化，esp32频率为80Mhz，80分频到1MHz
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &InterruptEvent, true);
  //32us中断一次(实际应该31.415926us这样设置会导致实际频率偏低一丢丢)
  timerAlarmWrite(timer, 32, true);
  timerAlarmEnable(timer);
}

void loop(){
  value = sin(angle/1000.0)*63+192;
  dacWrite(25, value);
  if(angle>=31415926){angle = 0;}
}

```
显然我们只需要对这个信号通过调频方式编码即可，实测输出信号频偏在2%以内(应该主要是因为定时器中断计数舍弃小数导致的偏少)。

如果我想传输状态改变频率为200Hz，信号频率800Hz以上比较保险，按照不同频率间隔40Hz算，从800Hz到1440Hz有16个频率每次可以传输4个比特，也就是100个字节每秒，完全可以满足GPS位置信息的传输速率要求（也许实际不行或更好只能等到实践的时候检验了）

有空测试一下电台的输入能不能是方波，如果可以这样可以大幅提高传输速率

## 数据编码

# 地面接收
## 频谱计算
这部分直接ADC采样然后FFT计算：
```c
#include "arduinoFFT.h"
#define SAMPLES 1024             //采样点，必须是2的指数
#define SAMPLING_FREQUENCY 10000 //采样频率(Hz)，由于adc限制应该小于10k

arduinoFFT FFT = arduinoFFT();
unsigned int sampling_period_us;
unsigned long microseconds;
double vReal[SAMPLES];
double vImag[SAMPLES];
 
void setup() {
    Serial.begin(115200);
    sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY));
}
 
void loop() {
    /*ADC采样*/
    for(int i=0; i<SAMPLES; i++){
        microseconds = micros();    //Overflows after around 70 minutes!
        vReal[i] = analogRead(34);
        vImag[i] = 0;
        while(micros() < (microseconds + sampling_period_us)){
        }
    }

    /*FFT计算*/
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
    double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
 
    /*输出主要频率计算结果*/
    Serial.println(peak);

    /*输出全部计算结果
    for(int i=0; i<(SAMPLES/2); i++){
      Serial.print((i * 1.0 * SAMPLING_FREQUENCY) / SAMPLES, 1);
      Serial.print(" ");
      Serial.println(vReal[i], 1);
    }*/
    delay(100);
}
```
## 数据解码

