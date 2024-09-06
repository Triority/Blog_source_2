---
title: 一些常见的一行命令小问题
date: 2022-07-12 16:25:00
tags:
- 笔记
description: 总有那么一些小问题，一行命令就能解决，但是这一行似乎永远记不住......
cover: /img/tips.png
categories: 
- 文档&笔记
---
## windows清除原有SSH公钥
在powershell输入：
```
~/.ssh/known_hosts
```
选择记事本打开方式，然后ctrl+a,然后delete

## 连接状态为Attached的screen
```
screen -D  -R <session>
```
## systemctl常用命令
```
#启动
sudo systemctl start frpc 
#关闭
sudo systemctl stop frpc
#重启
sudo systemctl restart frpc
#查看状态
sudo systemctl status frpc
#设置为开机自启动
sudo systemctl enable frpc
```
## 安卓子系统安装apk
```
adb connect 127.0.0.1:58526
```
```
adb install xxx.apk
``` 
```
PS C:\Users\Triority\Desktop> adb connect 127.0.0.1:58526
connected to 127.0.0.1:58526
PS C:\Users\Triority\Desktop> adb install base.apk
Performing Streamed Install
Success
PS C:\Users\Triority\Desktop>
```