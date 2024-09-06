---
title: Orange pi 5 plus开发板在ubuntu系统下使用docker安装openwrt
tags:
  - 香橙派
  - linux
cover: /img/pi5-plus-5.png
categories:
  - 折腾记录
date: 2024-04-10 19:28:10
description: 买了个香橙派导致的
---
# 硬件设备
香橙派新出了一个orangepi 5 plus，外设非常适合日常折腾，两个2.5G网口，两个USB3.0，还有pciex4的2280规格m2硬盘接口，算力也是足够强大，CPU是著名的RK3588，NPU算力6TOP，完全可以胜任绝大多数任务。于是入手一个8G内存版本，可以作为软理由+NAS，日常挂载一些服务也毫无压力

| ![](pi5-plus-17.png) | ![](pi5-plus-16.png) |
| :---: | :---: |
| 正面 | 背面 |

原计划是作为主路由用的，但是由于没有认真阅读官方文档，官方出售的orangepi5plus专用网卡是不支持openwrt镜像的，本来想自己打个驱动，然后看了一下发现官方没做支持是有原因的。只好拿来做旁路由，除非再去买支持的ax200或ax210芯片的网卡

# 在docker内安装openwrt
这是我第一次使用docker，但是配置过程还算顺利，指只折腾我一个下午然后发现原因是ip写错了才不能用

首先拉取docker镜像，我使用的镜像是这个:
```
https://hub.docker.com/r/sulinggg/openwrt
```
作者还为我们提供了不同CPU架构下的阿里云镜像站地址，RK3588是ARMv8架构，so
```
docker pull registry.cn-shanghai.aliyuncs.com/suling/openwrt:armv8
```
然后开始网路配置，打开网卡混杂模式，首先查看网卡名称：
```
root@orangepi5plus:~# ifconfig
docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:2e:0e:eb:05  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enP3p49s0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether c0:74:2b:fe:72:fc  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 142

enP4p65s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.125  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::42e5:883e:acef:1760  prefixlen 64  scopeid 0x20<link>
        ether c0:74:2b:fe:72:fd  txqueuelen 1000  (Ethernet)
        RX packets 32116  bytes 6923836 (6.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 51813  bytes 23028566 (23.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 154

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 29409  bytes 19939785 (19.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 29409  bytes 19939785 (19.9 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlP2p33s0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether c2:4b:24:c1:3e:d4  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether c0:4b:24:c1:3e:d4  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
可以看出设备的网卡`enP4p65s0`及当前的IP地址是`192.168.1.125`，然后打开这个网卡的混杂模式：
```
sudo ip link set enP4p65s0 promisc on 
```
然后为未来的容器创建一个网络：
```
docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=enP4p65s0 macnet
```
如果网段不一致要修改成使用环境下的网段

然后就可以创建和启动容器了：
```
docker run --restart always --name openwrt -d --network macnet --privileged registry.cn-shanghai.aliyuncs.com/suling/openwrt:armv8 /sbin/init
```
这是设置了容器总是自动重启，名称为`openwrt`，`-d`参数为容器运行在 Daemon 模式，加入`macnet`网络，`--privileged` 参数定义容器运行在特权模式下，启动命令是`/sbin/init`

接下来进入容器，修改相关配置：
```
docker exec -it openwrt bash
```
首先，我们需要编辑 OpenWrt 的网络配置文件:
```
nano /etc/config/network
```
更改 Lan 口设置：
```
config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option ipaddr '192.168.1.126'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option gateway '192.168.1.1'
        option broadcast '192.168.1.255'
        option dns '192.168.1.1'
```
注意由于已经在容器的虚拟环境下这时的网卡已经是`eth0`，以及`ipaddr`是访问`openwrt`的地址而不是开发板本身的地址，开发板是`192.168.1.125`，为了方便我就给`openwrt`地址`192.168.1.126`
```
bash-5.1# ifconfig
br-lan    Link encap:Ethernet  HWaddr 02:42:C0:A8:01:02
          inet addr:192.168.123.100  Bcast:192.168.123.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:34 errors:0 dropped:0 overruns:0 frame:0
          TX packets:58 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:2648 (2.5 KiB)  TX bytes:6292 (6.1 KiB)

eth0      Link encap:Ethernet  HWaddr 02:42:C0:A8:01:02
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:37 errors:0 dropped:0 overruns:0 frame:0
          TX packets:59 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:3304 (3.2 KiB)  TX bytes:7335 (7.1 KiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:20 errors:0 dropped:0 overruns:0 frame:0
          TX packets:20 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:1760 (1.7 KiB)  TX bytes:1760 (1.7 KiB)
```
重启网络：
```
/etc/init.d/network restart
```
之后就可以打开`192.168.1.126`的openwrt后台了，默认账号`root`密码`password`、

# openwrt配置
