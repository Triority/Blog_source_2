---
title: python的socket连接编程
tags:
  - python
cover: /img/5af741ba43356384ace081fe1d15371.jpg
categories:
- 文档&笔记
date: 2023-07-01 02:57:21
description: 使用python进行网络收发编程的常用代码记录
---
# 创建socket对象
在使用socket之前，必须先创建 socket 对象
```
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
```
前2个参数比较重要，其中：
+ `family` 参数用于指定网络类型。该参数支持 `socket.AF_UNIX`（UNIX 网络）、`socket.AF_INET`（基于 IPv4 协议的网络）和 `socket.AF_INET6`（基于 IPv6 协议的网络）这三个常量。
+ `type` 参数用于指定网络 Sock 类型。该参数可支持 `SOCK_STREAM`（默认值，创建基于 TCP 协议的 socket）、`SOCK_DGRAM`（创建基于 UDP 协议的 socket）和 `SOCK_RAW`（创建原始 socket）。一般常用的是 `SOCK_STREAM` 和 `SOCK_DGRAM`。


socket 对象提供了如下常用方法：
+ `socket.accept()`：作为服务器端使用的 socket 调用该方法接收来自客户端的连接。
+ `socket.bind(address)`：作为服务器端使用的 socket 调用该方法，将该 socket 绑定到指定 address，该 address 可以是一个元组，包含 IP 地址和端口。
+ `socket.close()`：关闭连接，回收资源。
+ `socket.connect(address)`：作为客户端使用的 socket 调用该方法连接远程服务器。
+ `socket.connect_ex(address)`：该方法与上一个方法的功能大致相同，只是当程序出错时，该方法不会抛出异常，而是返回一个错误标识符。
+ `socket.listen([backlog])`：作为服务器端使用的 socket 调用该方法进行监听。
+ `socket.makefile(mode='r', buffering=None, ＊, encoding=None, errors=None, newline=None)`：创建一个和该 socket 关联的文件对象。
+ `socket.recv(bufsize[, flags])`：接收socket 中的数据。该方法返回 bytes 对象代表接收到的数据。
+ `socket.recvfrom(bufsize[,flags])`：该方法与上一个方法的功能大致相同，只是该方法的返回值是 (bytes, address) 元组。
+ `socket.recvmsg(bufsize[, ancbufsize[, flags]])`：该方法不仅接收来自 socket 的数据，还接收来自 socket 的辅助数据，因此该方法的返回值是一个长度为 4 的元组 (data, ancdata, msg_flags, address)，其中 ancdata 代表辅助数据。
+ `socket.recvmsg_into(buffers[, ancbufsize[, flags]])`：类似于 socket.recvmsg() 方法，但该方法将接收到的数据放入 buffers 中。
+ `socket.recvfrom_into(buffer[, nbytes[, flags]])`：类似于 socket.recvfrom() 方法，但该方法将接收到的数据放入 buffer 中。
+ `socket.recv_into(buffer[, nbytes[, flags]])`：类似于 recv() 方法，但该方法将接收到的数据放入 buffer 中。
+ `socket.send(bytes[, flags])`：向socket 发送数据，该 socket 必须与远程 socket 建立了连接。该方法通常用于在基于 TCP 协议的网络中发送数据。
+ `socket.sendto(bytes, address)`：向 socket 发送数据，该 socket 应该没有与远程 socket 建立连接。该方法通常用于在基于 UDP 协议的网络中发送数据。
+ `socket.sendfile(file, offset=0, count=None)`：将整个文件内容都发送出去，直到遇到文件的 EOF。
+ `socket.shutdown(how)`：关闭连接。其中 how 用于设置关闭方式。


# TCP
## Server
```
# 导入 socket 模块
import socket
# 创建socket对象
s = socket.socket()
# 将socket绑定到本机IP和端口
s.bind(('127.0.0.1', 30000))
# 服务端开始监听来自客户端的连接
s.listen()
while True:
    # 每当接收到客户端socket的请求时，该方法返回对应的socket和远程地址
    c, addr = s.accept()
    print(c)
    print('连接地址：', addr)
    c.send('您好，您收到了服务器的新年祝福！'.encode('utf-8'))
    # 关闭连接
    c.close()
```
## Client
```
# 导入socket模块
import socket
# 创建socket对象
s = socket.socket()
# 连接远程主机
s.connect(('127.0.0.1', 30000))    # ①
print('--%s--' % s.recv(1024).decode('utf-8'))
s.close()
```
# UDP
## Client
```
# 1、导入模块
import socket

# 2、创建套接字
udp_socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 3、发送信息到服务器
udp_socket_client.sendto("hello".encode("GBK"), ("127.0.0.1", 8080))
# 4、接收服务器回复的信息并解码 显示
recv_data, ip_port = udp_socket_client.recvfrom(1024)
print("服务端回复信息：%s" % recv_data.decode("GBK"))
print("服务端IP及端口", ip_port)
# 5、关闭套接字
udp_socket_client.close()

```
## Server
```
# 1、导入模块
import socket

# 2、创建套接字
udp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 3、绑定服务端的IP和端口
udp_socket_server.bind(("127.0.0.1", 8080))
# 4、接收客户端的信息
recv_data, ip_port = udp_socket_server.recvfrom(1024)
# 5、解码接收到的信息并显示
recv_str = recv_data.decode("GBK")
print("接收到客户端发送的数据:%s" % recv_str)
print("客户端IP及端口", ip_port)
# 6、回复信息给客户端
udp_socket_server.sendto("服务端收到信息啦！".encode("GBK"), ip_port)
# 7、关闭套接字
udp_socket_server.close()

```