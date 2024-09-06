---
title: syncthing发现和中继服务器的搭建
date: 2023-01-06 22:39:17
tags:
- 教程
description: 搭建自己的syncthing发现和中继服务器以加快速度和提高稳定性
cover: /img/syncthing.png
categories: 
- 折腾记录
---
## 折腾的借口
前段时间用sync同步手机电脑文件，简直太舒服，唯一问题就是公共的中继服务器网络质量参差不齐，于是打算自己搭建一个发现和中继服务器，提高速度和稳定性。

## 搭建发现服务器 Syncthing Discovery Server
### 下载 stdiscosrv 程序

[stdiscosrv](https://github.com/syncthing/discosrv/releases)

```
wget https://github.com/syncthing/discosrv/releases
```

解压后运行：

```
./stdiscosrv
```

虽然需要密钥，但是就算不配置程序启动后也会自动生成

### 启动参数
如果需要修改端口，启动时可以加参数`-listen=<address>`，默认端口为`8443`。其他参数不是很常用，需要可以去看[文档](https://docs.syncthing.net/users/stdiscosrv.html#syncthing-discovery-server)

## 搭建中继服务器 Syncthing Relay Server
[relaysrv](https://github.com/syncthing/relaysrv/releases)

```
wget https://github.com/syncthing/relaysrv/releases
```

解压后运行

```
./stdiscosrv
```

虽然也需要密钥，但是跟刚才一样就算不配置也可以
### 启动参数-重要！

+ 全局限速：`-global-rate=<bytes/s>`
+ 创建私人服务器`-pools=""`，如果没有这一参数，网络上所有人都可以用你的服务器流量进行免费传输

### 运行(私人中继服务器)
```
./strelaysrv -pools=""
```

## 客户端配置
运行程序后会生成一个`id`，将其拷贝下来

发现服务器：
> https://ip_address:port/?id=your_id

中继服务器:
> relay://ip_address:port/?id=your_id

自己的地址可以用逗号和`default`分开，这样就能同时使用多个地址。

比如我的：

协议监听地址：
```
tcp4://0.0.0.0:22000,relay://triority.cn:22067/?id=your_id
```

全局发现服务器
```
https://triority.cn:8443/?id=your_id, default
```

