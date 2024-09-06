---
title: SDR使用FT8模式通联信号接收
tags:
  - 无线电
cover: /img/88057845a059ca6c10a9feb6498515d.png
categories:
  - 无线电
date: 2024-04-13 20:21:30
description: 
---
# FT8简介
```
FT8 于 2017 年 7 月推出，由 Steve Franke ，K9AN 和 Bill Somerille，G4WJS 制作。
设计用于 6 米波段的突发 E 层通联，然后被引入短波，迅速风靡全球。
和 JT65 一样，它不适合随意聊天，仅仅是为了完成最基本的通联

FT8 极强的弱信号通联为很多短波爱好者提供了更多的 DX 机会。
FT8 减少了人类活动的参与，降低了错误的出现，效率极高。
可以在很短的时间内获取更多的 DXCC。7天时间完成DXCC100，FT8创造奇迹

---- BH4IWK
```


```
场景：BG2KSI在PN33进行CQ，BG2XXX在PN35抄收并回复，并假定双方接收的信号报告均为-10
BG2KSI：CQ BG2KSI PN33
BG2XXX：BG2KSI BG2XXX PN35
BG2KSI：BG2XXX BG2KSI -10
BG2XXX：BG2KSI BG2XXX R -10
BG2KSI：BG2XXX BG2KSI RR 73
BG2XXX：BG2KSI BG2XXX 73

以上内容含义如下：
BG2KSI：CQ 我是BG2KSI 我的位置是PN33
BG2XXX：BG2KSI 我是BG2XXX 我的位置是PN35
BG2KSI：BG2XXX 我是BG2KSI 我收到你的信号报告为-10
BG2XXX：BG2KSI 我是BG2XXX 收到 我收到你的信号报告为-10
BG2KSI：BG2XXX 我是BG2KSI 收到收到 73
BG2XXX：BG2KSI 我是BG2XXX 73

---- BG2KSI
```

# 软件

+ SDRuno(SDR信号接收)
+ [VB-Audio cable(虚拟声卡)](VBCABLE_Driver_Pack43.zip)
+ JTDX(FT8信号解码)
+ GridTracker(可选，网格可视化)

# 使用
QTH：北京市海淀区学院路某楼9层向东阳台
SDR：RSP1(BG7YZF)
ANT：有源小环天线(BG7YZF)
FREQ：10.136MHz
TIME：文章创建时间

![](88057845a059ca6c10a9feb6498515d.png)

可能是天线朝向原因收到几个十分活跃的日本友台，以及一些中国韩国俄罗斯友台

第一次尝试不过感觉有点怪，虽然FT8据说十分流行，但是通联成为了电脑全自动完成的过程还是少了很多乐趣，不过FT8的弱信号接收能力是真的强，这一点真的离谱

![](c7c9077c6632ce35692c4fa5dcf36b9.png)

要是SSB模式你跟我说这是有信息？？？
