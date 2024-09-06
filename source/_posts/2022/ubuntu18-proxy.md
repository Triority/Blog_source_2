---
title: ubuntu18搭建代理服务器
date: 2022-07-16 19:17:54
tags:
- linux
- 教程
description: 近期买了一个印度的服务器，搭建一个代理服务器玩一玩
cover: /img/ubuntu18-proxy.png
categories: 
- 折腾记录
---
# 仅供学习请勿用于其他用途！

## 安装
```
sudo apt-get install tinyproxy
```
## 编辑配置文件
```
sudo nano /etc/tinyproxy/tinyproxy.conf 
```
一般需要修改的内容是：
`Port 8888 `改成自己喜欢的端口
`Allow 127.0.0.1 `改为`#Allow 127.0.0.1 `也就是注释掉，就可以不进行ip验证
`BasicAuth [Username] [Password]`可以在此设置授权

## 服务
```
sudo service tinyproxy start
sudo service tinyproxy stop
sudo service tinyproxy status
sudo service tinyproxy restart
```
## 开机自启
```
systemctl enable tinyproxy.service
```
## 完成