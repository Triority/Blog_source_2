---
title: server-Services
tags:
  - linux
cover: /img/loading.gif
notshow: true
date: 2023-01-31 18:29:21
categories:
- 文档&笔记
description: 服务器服务记录，用于在服务器重启后启动(毕竟不是经常重启懒得写成服务了)
---
# 必须
## Frps
```
screen -R frps
cd /frps
./frps -c frps.ini
```
## strelaysrv
```
screen -R strelaysrv
cd /strelaysrv
./strelaysrv -pools=""
```
## stdiscosrv
```
screen -R stdiscosrv
cd /stdiscosrv
./stdiscosrv
```
## cloudreve
```
screen -R cloudreve
cd /cloudreve
./cloudreve
```
## library
```
screen -R library
cd /library
cps
```
# 可选
## syncthing
```
screen -R syncthing
cd /syncthing
syncthing
```