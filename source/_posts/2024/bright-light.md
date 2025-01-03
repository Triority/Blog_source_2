---
title: 一个“比较亮”的手电
tags:
  - 电力电子
  - PCB设计
  - stm32
cover: /img/微信截图_20241210150036.png
categories:
  - 折腾记录
date: 2024-12-10 13:13:13
description: 手电筒，但是300W，70000lm
---
# 想法
做这个的想法大部分来源于有一天晚上，走G6辅路从昌平骑车回市内，一堆解限速横冲直撞的逆行远光电动车给我整破防了，想做个小手电制裁一下。起因只是这么简单但是考虑到其他无辜的人我也不会真的这样去做，但是发现这个东西好像确实需要，用来摄影打光，以及夜间外出徒步这类活动都可以用，所以还是决定做出来

另一方面，关于这个手电的电源。绝大部分的设计方案都是使用一颗升压芯片来做电源控制，但是我这里有些别的想法。我以后会做一个大功率自动升降压可调电源，正好可以在这里复用，就当提前踩个坑了，所以虽然会更贵一点，我决定供电方案采用buck-boost自动升降压的恒定电流控制，顺便兼容一下各种电压的电池

至于控制芯片，考虑到这个功能不算复杂，以及我想拿stm32练练手但是用的机会不多，就用stm32f103c8t6做主控吧

# 设计方案
## LED
这部分没啥技术含量，找个光效高功率大的灯就完了，这里我选择了立德达的5050贴片LED，光效250lm/w，显色指数70，电压选择了6V。随手画一个2串50并的铝基板灯板。按照规格书的功率最大值，单个功率3W，光通量700lm，总计12V 25A 300W功率，70000流明。

| ![](微信截图_20241210150050.png) | ![](微信截图_20241210150036.png) |
|:---:|:---:|
| [原理图](ProDoc_P1_2024-12-10.epro) | [PCB](ProDoc_PCB1_(6V)_2024-12-10.epro) |
| <img width=2000/> | <img width=2000/> |

## 制冷
最大300W的功率，按照LED光源30%的效率计算，会有210W发热，再加上我打算超过规格书的范围继续过流和安全余量，总之散热按照400W设计。想都不要想，直接上水冷！

冷头使用60x60mm的铝制水冷头，搭配150x40x40的服务器冷排，在手电筒的体积内散热400W已经完全足够了。

## 供电
供电需要恒流控制下的大约12V电压，正常情况下电流需要25A，考虑到疯狂的我估计会超频和安全余量，所以按照到40A设计。

以及恒压5V供电给冷排散热风扇，3.3V给主控电路。这部分直接用buck降压电路和LDO芯片解决了没啥可说的。

# 成品

