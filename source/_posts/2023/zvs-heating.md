---
title: 无抽头zvs感应加热
tags:
  - 电磁炉
  - PCB设计
  - 电力电子
cover: /img/
categories:
- 折腾记录
date: 2023-01-15 15:43:33
description: 来自与立创开源广场的电路
---
## 两个电路
这两个电路来自立创开源广场，区别在于功率不同，一个使用两个MOS管，一个用4个。前段时间不是在研究`电磁炉`的升压电路嘛，和这个原理几乎一样。原文写的图片过多，翻找起来十分麻烦，所以在这转载一下。

#### 开源协议是`WTFPL`：
> WTFPL许可协议全文：
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE Version 2, December 2004Copyright (C) 2004 Sam Hocevar. Everyone is permitted to copy and distribute verbatim or modifiedcopies of this license document, and changing it is allowed as longas the name is changed.DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSETERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION0. You just DO WHAT THE FUCK YOU WANT TO.
#### 原文链接
|[无抽头ZVS感应加热2管](https://oshwhub.com/Soviet_lynx/ZVS_IH_2MOS)|[无抽头ZVS感应加热4管](https://oshwhub.com/Soviet_lynx/ZVS_IH_4MOS)|
|---|---|
| ![2管](bDsezGxEpgbfMpKnHknjMGEE1yTeO0wyBEsdJ9hY.jpg) | ![4管](jVguS5GzsHfRpJrIeYpbb1z78IkyzdpDvxvyisaf.jpg) |

[4管版本演示视频](https://www.bilibili.com/video/BV1mX4y1u7gN)

## 原理图及BOM
### 两管

> 2管的ZVS感应加热，功率管型号使用了IRFP260 场效应管，48V（53.5V）下工作，最大可以运行在1.5kW。

![2管](wtqZ1Dcx43DrFtgx7jA72eU9LiCVK1J7cgHrtZmB.png)

Q1，Q2 ：IRFP260   2个
L1，L2：100uH 15A 2个
D1，D2：FR307        2个
D4，D5：1N4742     2个
R4，R5：10K 0.25W 2个
R2，R3：470R到750R，可根据实际情况调阻值，两个电阻的阻值要一样  2个
谐振电容：1200V 0.33uf 6个 ，（可直接联系丰明或者创格厂家定做，立式电容。）
R1：10K 0.25W  1个
LED ：5mm  颜色任意 1个
P2，P1：M4铜柱，高度30mm ， 6个

### 四管
![4管](x2azPc11vUShhwYlsvT5E2dJdlmoQ41MLQUG9xkM.png)

C1, C2 : 1200V 0.33 电磁炉电容 12个
D1, D2: FR307 2个
D3: 5mm LED 1个
D4, D5, D6, D7:1N4742 4个
L1, L2: 100uH,20A 2个
P1:HB9500-2P 1个
P2, P3, P5:XH2.54/2P 3个
P4, P7, P8, P10: M4铜柱，高度30mm ， 6个
P6, P9：PCB-10端子 2个
Q1, Q2, Q3, Q4：IRFP260 4个
R1, R4, R5, R6, R7：10K，0.25W
R2, R3：470R 5W RX27-5

### 其他元件

> 水泵，可以在淘宝买隔膜泵，买带电源的就行。
> 
> 风机，买48V的12025或者12038的高速风机。注意风机的正负极不要插错，不能使用金属风机。
>
> 关于通信电源的选购，可以在咸鱼去找华为R4850或者R4875，中兴ZXD3000或者ZXD4000，台达4856。这东西新旧都有，看自己喜好。
>
> 关于加热线圈，如果是用于坩埚，那就把坩埚买来了在石英坩埚上面盘铜管，绕满就行。如果用于其他工件的加热，根据实际情况去做。线圈的直径越大，圈数越多，所需功率越大。一般用于直径60mm以下的工件加热，加热的时候注意耦合度，注意监测电流不要过载。
>
> 坩埚可以在淘宝买1kg坩埚套装，也可以用下面的小坩埚。

![坩埚](PFyejGpA1QPrCeGvYZDhj5dvLOKCiq5ttLzTdasK.jpg)

![散热片尺寸](ikEJdLdoSprsMhK5HF8YuVpQlf5mlbOccPjTIG5Q.png)

## PCB
[两管](https://lceda.cn/editor#project_id=b7443b19f4f0441da76def948c7d31c9)

[四管](https://lceda.cn/editor#project_id=3fd16e4140594e3c8e97fd7ad751a1b2)