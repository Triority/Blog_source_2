---
title: 非常离谱的MC服务端启动程序
tags:
  - python
  - minecraft
cover: /img/微信图片_20240520212634.png
categories:
  - 整活&游戏
  - 折腾记录
date: 2024-05-20 21:21:40
description: 主打一个，花里胡哨
---
本来是想写一个服务端自动重启的，但是闲的没事往里加了点别的功能，比如自动启动frp内网穿透，以及没有任何意义的等待进度条。如果以后更加无聊也许会往里增加更多没卵用的功能，比如frp的控制？
```py
# minecraft
server_jar_path = "server.jar"
java_Xms = "1024M"
java_Xmx = "4096M"
# frp
frp_enable = True
frp_dir_path = "frpc\\"

# something useless
import os,time,sys
GREEN_TEXT = ('\033[92m', '\033[0m')


def frp_thread_func(frp_dir_path):
    print (GREEN_TEXT[0] + "Frpc thread starting" + GREEN_TEXT[1])
    os.system(".\\" + frp_dir_path+ "frpc -c " + frp_dir_path + "frpc.ini")


if frp_enable:
    import _thread
    try:
        _thread.start_new_thread(frp_thread_func, (frp_dir_path, ))
        time.sleep(5)
    except:
        print(GREEN_TEXT[0] + "Frp thread Error" + GREEN_TEXT[1])


def progress_bar():
    for i in range(1, 101):
        print("\r", end="")
        print("Waiting: {}%: ".format(i), "▋" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(0.05)
    print("")


while True:
    print(GREEN_TEXT[0] + "Minecraft server Starting: ----- " + time.asctime(time.localtime(time.time())) + GREEN_TEXT[1])
    try:
        os.system("java -Xmx" + java_Xmx + " -Xms" + java_Xms + " -jar " + server_jar_path + " nogui")
    except:
        print(GREEN_TEXT[0] + "ERROR, Stopped" + GREEN_TEXT[1])

    try:
        time.sleep(3)
        print(GREEN_TEXT[0] + "Server Stopped. Restart in 5 seconds. Press Ctrl+C to exit." + GREEN_TEXT[1])
        progress_bar()
    except KeyboardInterrupt:
        print(GREEN_TEXT[0] + "EXIT" + GREEN_TEXT[1])
        exit()

```
实现效果：
![](微信图片_20240520212634.png)