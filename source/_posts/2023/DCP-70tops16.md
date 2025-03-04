---
title: 电磁炉：使用晶闸管半控制
tags:
  - 电磁炉
  - 电力电子
  - PCB设计
cover: /img/v2-100f3b14743b9c8fe3e58536acaa072c_r.png
categories:
- 折腾记录
date: 2023-1-13 12:18:43
description: 使用晶闸管70tops16的初始版本
---
# 潘多拉魔盒
这个实际上是在2022.11.1做的，当时没有整理东西写篇文章，现在补一下

做这个属实是心血来潮当天晚上没回去宿舍，在实验室没什么事干，直接动手开始搓的，技术上十分简单就是用晶闸管控制电容放电，一次成功玩了一晚上hhhc

这个电路图来源于淘宝商家电磁爱好，当天晚上就是直接用电线焊接的电路，没用洞洞板或者PCB，本来计划做三级加速，但是因为ABS管受热变形最后只能做一级加速

![电路图](tb_image_share_1673668494913.jpg)

做完之后效果如下：

{% dplayer "url=https://cr.triority.cc/f/10UP/VID_20221102_044358.mp4" %}

实测使用6mm直径的钢珠有一定概率打穿易拉罐

![饮料瓶](IMG_20221102_045138.jpg)

22年末北京发生了一些事情(嗯对因为疫情)，11月份就放假回家了，所以当时被迫中止

# 整合一下：2023.10.13

原以为晶闸管的故事在11个月前就应该结束了，知道昨天我用RLC工具做了仿真，使用IGBT可控关断和晶闸管直接控制相比，在三级加速以内竟然是晶闸管更有优势。

主要原因是IGBT有电流的限制，例如我用的4067D，保守一点最大电流400A，而使用70tps16电流1000A不成问题，于是反而前几级更适合使用晶闸管。所以如果至少想做一个非常小的三四级加速的，晶闸管控制又便宜又好。

很巧70tps16和4067D的引脚顺序刚好相反，也就是是为4067D设计的板子可以把管子方向掉转180度，直接用于驱动70tps16。因此我就用[原本为4067D设计的PCB了](https://triority.cc/2023/DCP-GPS4067D/#%E7%94%B5%E8%B7%AF%E8%AE%BE%E8%AE%A11-0)：

PC817C最大驱动电流是100mA，而70tps16驱动电流刚好100mA，所以去掉两个稳压二极管就可以直接拿来用了，IGBT留着直接去做半桥吧

# 害怕炸管，随手重画：2023.10.14
如本段标题所示，担心光耦电流不够所以再加一个三极管放大吧，顺便去掉两个稳压二极管，以及两级放在一个板子上方便安装

| ![](微信截图_20231014171245.png)  | ![](微信截图_20231014171259.png)  | ![](微信截图_20231014171323.png)  |
| :------------: | :------------: | :------------: |
| 原理图  | PCB  | 3D模型  |

实测这个也有些问题，三极管如果长时间道通会因为过流损坏，因此要么改PCB加上限流电阻，要么减少导通时间。显然我选择了后者因为我懒hhhhhhhhhc

# 叠层
上面那个设计上还是有缺陷，长时间导通可能导致三极管过流烧毁，所有又做了一个，加上好几个限流电阻，同时为了在大电容的情况下减小总体积使用的叠层结构

这个版本做了两个，第一次只是加上了限流电阻，但是铺铜层忘记增大到高电压走线的规避距离导致击穿，同时这次结构磁感线在控制电路里可以产生回路极易导致误触，因此删掉了三极管放大，反正不加也能用

| ![](814b854a0605f40f383bba870886a4e.jpg)  | ![](11e431f3c8ccea551ba5def4198345b.jpg)  |
| :------------: | :------------: |
| 组装  | 击穿处  |

做的新的直接去掉了铺铜，看原理图有一种返璞归真的感觉：

| ![](QQ截图20231231234030.png)  | ![](QQ截图20231231234043.png)  | ![](QQ截图20231231234109.png)  |
| :------------: | :------------: | :------------: |
| 原理图  | PCB  | 3D模型  |

# 控制程序
考虑到还要根据实际情况调参，这里时间和引脚配置没有直接int而是写了个数组，等我不懒的时候会改成串口调参

```
// 三极管导通时间(us)
int time_trigger = 10;
// 级数
int levels = 2;
// 每一级的控制引脚和下一级的间隔时间
int pin_delaymicros[4][2] = {
  {13,2000},
  {12,1000},
  {14,500},
  {27,250}
};

void setup() {
  Serial.begin(115200);
  for (int i=0;i<levels;i++){
    pinMode(pin_delaymicros[i][0], OUTPUT);
    digitalWrite(pin_delaymicros[i][0], LOW);
    Serial.print("初始化引脚：");
    Serial.println(pin_delaymicros[i][0]);
  }
  pinMode(0,INPUT);
  Serial.println("初始化完成等待触发...");
}

void loop() {
  if(digitalRead(0)==LOW){
    for (int i=0;i<levels;i++){
      digitalWrite(pin_delaymicros[i][0], HIGH);
      Serial.print("trigger:");
      Serial.println(pin_delaymicros[i][0]);
      delayMicroseconds(time_trigger);
      digitalWrite(pin_delaymicros[i][0], LOW);

      delayMicroseconds(pin_delaymicros[i][1]);
    }

    delay(2000);
  }
}
```

嗯串口调参也写完了博客发了也在github开源了(2023.12.31突然想起来补充)

# 器件参数
晶闸管70tps16参数如下
![](QQ截图20230626020054.png)
