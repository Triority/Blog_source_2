---
title: frpc-systemctl
date: 2022-09-29 02:17:30
tags:
- linux
description: 日常重建环境...之frpc...
cover: /img/frp.png
categories: 
- 文档&笔记
---
frp总是要去配置systemctl服务，所以复制粘贴什么的最棒了
首先编辑：
```
sudo nano /lib/systemd/system/frpc.service
```
然后写
```
[Unit]
Description=frpc service 
After=network.target syslog.target
Wants=network.target

[Service]
Type=simple
#frp路径
ExecStart=/usr/local/frpc/frpc -c /usr/local/frpc/frpc.ini
#自动重启
Restart=always
RestartSec=5
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
```
