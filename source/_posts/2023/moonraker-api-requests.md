---
title: 通过requests使用moonraker的api
tags:
  - 3D打印
cover: /img/moonraker.png
categories:
- 折腾记录
date: 2023-08-02 22:45:47
description: 通过python向moonraker发送api请求。至于封面，是一种很新的moonraker
---
想起来做这个主要是因为打印机这几天一直在高强度工作，但是热床预热需要五分钟时间，每次打印都要等五分钟很烦，打印机十分钟没有操作就会关掉加热，所以需要一个一直运行的程序保持唤醒。

moonraker开放webapi接口可以直接调用操作打印机，[官网文档](https://github.com/Arksine/moonraker/blob/master/docs/web_api.md)

按照文档中的说明，可以用python直接发送gcode给打印机执行：
```
Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> r = requests.post("http://192.168.0.104/printer/gcode/script?script=M220 S150")
>>> r.text
'{"result": "ok"}'
>>> r
<Response [200]>
>>>
```
此时打印机移动速度就变成了150%。或者你要是想要做个急停按钮可以用M112，或者直接post到`/printer/emergency_stop`也可以实现

接下来只要定时发这个gcode就可以保持打印机运行
