---
title: matlab的simulink进行简单的电力电子仿真：Buck电路
tags:
  - 电力电子
cover: /img/QQ截图20230912211748.png
categories:
- [折腾记录]
- [文档&笔记]
date: 2023-09-12 19:45:44
description: 电力电子仿真
---
# 主要目的
做这个主要是想给自己做个桌面电源，功率大一点(1kW+)那种，把平时经常用到但是实验室的电源不具备的功能尝试做一下。做的电源可能拉的时间线比较长，基本做出来之后再写个制作过程的文章

其实这个没什么难的，但是主要是各种常用元件的位置是真的记不住，写这个文章主要是方便以后再去找，所以说的可能不是特别细

# 在simulink搭建buck电路
## 基本电路搭建
新建一个仿真工程，在库浏览器中，依次打开`Simscape-Electrical-specialized Power System`，电力电子仿真所需的器件大都在这里

首先拖动`powergui`放在右边，然后在`sources`中找到需要的直流电源，在`power electronics`的二极管(doide)和mosfet，在`passives`中的RLC。

另外需要测量数值，放置一个`sensors and measurements`中的万用表(Multimeter)，以及根目录下`simulink`中`commonly used blocks`的示波器(Scope)，

对于控制mosfet，可以放一个位于根目录下`simulink`中`sources`的脉冲发生器(Pulse Generator)

然后设置一下仿真时间步长，在菜单栏的模型设置，默认的10s时间太长了，步长根据频率而定。

设置好电路参数，就可以进行电路布局和连线了，运行之后查看示波器：

![](QQ截图20230912204255.png)

## 输出闭环pid控制
根目录下`simulink`中`commonly used blocks`有一个`constant`可以表示一个常数，可以用于表示我们的目标电压，比如写一个12v，同目录下还有一个`sum`可以用于求和或者做差，当然我们就是做差了

减数就是输出的电压，可以放一个万用表并配置输出为负载电阻的电压

然后放置一个`simulink-continuous`里面的pid控制器(PID Controller)，输出的信号可以接一个`Simscape-Electrical-specialized Power System-Power Electronice-Power Electronice Control`PWM生成器(PWM Generator(DC-DC))然后就可以控制mosfet了

现在逻辑设置完就可以调节一下pid参数了，这里我随便设置了一个，输出电压的仿真结果如下：

![](QQ截图20230912211748.png)