---
title: nonebot2+cqhttp方案实现自定义Python插件的QQ机器人
description: 目前机器人框架有很多,框架内也有很多插件实现各种各样的功能.但是当我们想要的功能没有理想的插件可以实现时,也就需要自己编写一个插件.很多框架只支持易语言编写的插件,但是我个人认为易语言的编程体验十分不好,于是最终采用可以用python编写插件的nonebot框架+go-cqhttp方案
cover: /img/nonebot.png
date: 2022-01-22 16:54:02
categories: 
- [折腾记录]
- [作品&项目总结]
- [值得一提的文章]
tags:
- python
- QQ机器人
- linux
- 教程
---
## 前言

目前机器人框架有很多,框架内也有很多插件实现各种各样的功能.但是当我们想要的功能没有理想的插件可以实现时,也就需要自己编写一个插件.很多框架只支持易语言编写的插件,但是我个人认为易语言的编程体验十分不好,于是最终采用可以用python编写插件的nonebot框架+go-cqhttp方案

## 目标功能

为了管理一个千人QQ群,需要一个可靠且便利的方式来记录群员的违规行为,经过讨论,管理员们决定采用类似机动车驾驶证的记分制度.本文章即为实现记分并踢出记分达到指定分数的群员.

## nonebot2

nonebot的官方文档已经给出安装方法,在这里只大概记录一下.
**[nonebot2官方文档](https://v2.nonebot.dev/ "nonebot2官方文档")**

首先安装需要的库[需要Python3.7以上]
```python
pip install nb-cli==0.5.3
```
最新版本为0.6.4,但是这个版本安装nonebot时会有一些本人不会解决的麻烦,所以尝试了旧版本,可以正常运行

在机器人目录内安装
```python
nb
```
选择Create a New Project--输入项目名--选择第一项新建文件夹--载入 nonebot 内置插件--选择 cqhttp插件

此时就会生成机器人需要的文件,启动机器人只需要启动bot.py程序
```python
python3 bot.py
```
## Go-cqhttp
这就是一个QQ客户端,首先在github下载合适的文件
**[go-cqhttp下载](https://github.com/Mrs4s/go-cqhttp/releases "go-cqhttp下载")**
下载后启动:
```python
./go-cqhttp
```
会生成其配置文件,需要修改的是config.yml文件:
```python
xxxxxxxxxxxxxxxxx
    uin:      # 机器人QQ账号[密码不写,登陆时扫码登陆]
xxxxxxxxxxxxxxxxx
    universal: ws://127.0.0.1:8080/cqhttp/ws
xxxxxxxxxxxxxxxxx
```
再次启动go-cqhttp 

## 加载插件
在机器人目录的plugins目录内,新建lab.py作为插件,并修改bot.py以加载插件
```python
nonebot.init()
 
# load your plugin here
 
nonebot.run()
```
将# load your plugin here替换为
```python
nonebot.load_plugins("triority/plugins/lab.py")
```

## 编写插件
插件的编辑方法在官方文档中已经有所说明,在下面直接给出文章写到这时已经写完的代码

## 用于在QQ群记分的插件
这个程序仍然需要改进,比如不能使用at来选中成员而只能QQ号--这个已经于2022/5/14晚修复
经过测试如果记分没有写理由会导致分数增加但是没有计入明细--这个已经于2022/7/1晚修复，同时还加入了语法错误的回复
加入了ops随时修改的功能，但是必须由op列表内的人员进行修改--2022/7/3的更新
删除了对QQ群号的限制--2022/7/4的更新
```python
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message
import numpy as np
import datetime
op = ["123"]
#白名单ops
f = open("test.txt", "r",encoding='utf-8')
data = f.readline()
f.close()
ops = eval(data)
#记分
scores = np.load('scores.npy',allow_pickle=True).item()
keys = ['QQ号','查分','记分','明细','穷举','清零','计分','op','deop']
#回复部分
reply = on_message(priority=100)
@reply.handle()
async def reply_handle(bot: Bot, event: Event):
    try:
        #获取聊天内容user_msg
        user_msg = str(event.get_message()).strip()
        #获取发消息的人user,群号qun
        msg = str(event.get_session_id())
        user = msg.split("_")[2]
        qun = msg.split("_")[1]
        now = datetime.datetime.now()
        #消息空格分割列表words
        user_msg.rstrip()
        words = user_msg.split(' ')
        global len
        length = len(words)
        if words[0]=='QQ号' and words[1][1:6]=='CQ:at' and length==2 :
            await reply.finish(words[1][10:-1])
            return
        if user_msg[0:2]=='查分' and length==2:
            if words[1][1:6]=='CQ:at':
                words[1]=words[1][10:-1]
            if words[1] in scores:
                await reply.finish(words[1]+' 的记分为 '+str(scores[words[1]][0]))
                return
            else:
                await reply.finish(words[1]+' 无记分记录')
                return
        if user in ops :
            if user_msg[0:2]=='记分' and length==4 :
                if words[2][1:6]=='CQ:at':
                    words[2]=words[2][10:-1]
                if words[2] in scores:
                    scores[words[2]][0]=scores[words[2]][0]+int(words[1])
                    scores[words[2]].append([now.strftime("%Y-%m-%d %H:%M:%S"),words[1],words[3]])
                else:
                    scores[words[2]]=[int(words[1]),[now.strftime("%Y-%m-%d %H:%M:%S"),words[1],words[3]]]
                np.save('scores.npy', scores)
                await reply.finish(words[2]+' 当前记分为 '+str(scores[words[2]][0]))
                return
            if user_msg[0:2]=='清零' and length==2 :
                if words[1][1:6]=='CQ:at':
                    words[1]=words[1][10:-1]
                if words[1] in scores:
                    del scores[words[1]]
                    np.save('scores.npy', scores)
                    await reply.finish(words[1]+' 记分已清空')
                    return
                else:
                    await reply.finish(words[1]+' 无记分记录')
                    return
            if user_msg[0:2]=='明细' and length==2 :
                if words[1][1:6]=='CQ:at':
                    words[1]=words[1][10:-1]
                if words[1] in scores:
                    reason='总记分'+str(scores[words[1]][0])+':\n'
                    for i in range(1,len(scores[words[1]])):
                        reason=reason+str(i)+'.'+scores[words[1]][i][0]+'\n  记分数:'+scores[words[1]][i][1]+'\n  理由:'+scores[words[1]][i][2]+'\n'
                    await reply.finish(words[1]+' 记分明细如下:\n'+reason)
                    return
                else:
                    await reply.finish(words[1]+' 无记分记录')
                    return
            if user_msg[0:2]=='穷举':
                await reply.finish('全部记录如下:'+str(scores))
                return
        if words[0]=='op' and user in op and length==2:
            if words[1][1:6]=='CQ:at':
                words[1]=words[1][10:-1]
            if words[1] in ops:
                await reply.finish(words[1]+'已有权限')
            else :
                ops.append(words[1])
                f = open("test.txt", "w",encoding='utf-8')
                f.write(str(ops))
                f.close()
                await reply.finish(words[1]+'成功获得权限')
            return
        if words[0]=='deop' and user in op and length==2:
            if words[1][1:6]=='CQ:at':
                words[1]=words[1][10:-1]
            if words[1] in ops:
                ops.remove(words[1])
                f = open("test.txt", "w",encoding='utf-8')
                f.write(str(ops))
                f.close()
                await reply.finish(words[1]+'已被删除权限')
            else :
                await reply.finish(words[1]+'并没有权限')
            return
        if words[0] in keys and user in ops:
            await reply.finish('您输入的语法有误，如有问题请查看机器人说明书：http://triority.cn/2022/06/16/how-to-use-qqbot/')
    except KeyError:
        await reply.finish()

```

## 用于在QQ群中发送MC服务器rcon命令的插件
这个插件同样有带完善,如果无法连接至rcon服务端,可能导致进程一直卡在建立连接,同上,有待完善
作为一个好腐竹只需在QQ群中发送`rcon name kill @e`即可提高你的威望
import的rcon库在插件的代码下面
```python
from rcon import MCRcon
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message
 
def rcon_send(ip,port,key,command):
    with MCRcon(ip, key, port ) as mcr:
        resp = mcr.command(command)
        return resp
 
servers={'name':["ip",port,'key',['op']]
         }
 
reply = on_message(priority=100)
 
@reply.handle()
async def reply_handle(bot: Bot, event: Event):
    try:
        #获取聊天内容user_msg
        user_msg = str(event.get_message()).strip()
        #获取发消息的人user,群号qun
        msg = str(event.get_session_id())
        user = msg.split("_")[2]
        qun = msg.split("_")[1]
        # 消息空格分割列表words
        words = user_msg.split(' ')
        if words[0] == 'rcon':
            if words[1] not in servers:
                await reply.finish('服务器未被记录')
            elif user in servers[words[1]][3]:
                try:
                    ret = rcon_send(servers[words[1]][0], servers[words[1]][1], servers[words[1]][2], words[2])
                    await reply.finish(ret)
                except:
                    await reply.finish('无法连接至服务器rcon')
            else:
                await reply.finish('您没有连接服务器的权限')
    except KeyError:
        await reply.finish()
```
### rcon库--由老咩友编写
他的github[链接](https://github.com/Redroadsl/Minecraft-Rcon "链接")
```python
import socket
import ssl
import select
import struct
import time
#导入模块

class MCRconException(Exception):
    pass


class MCRcon(object):	
    """Minecraft服务端远程命令（RCON）模板

	老咩友情提醒您：
		道路千万条，
		规范第一条。
		写码不规范，
		维护两行泪。

    推荐你使用python的'with'语句！
    这样可以确保及时的关闭连接，而不是被遗漏。

    'with'语句例子:
    In [1]: from mcrcon import MCRcon
    In [2]: with MCRcon("这是一个ip", "这是rcon的密码","这是Rcon的端口" ) as mcr:
       ...:     resp = mcr.command("/发送给服务端的指令")
       ...:     print(resp) #输出

	
	两行泪方式:
	你当然也可以不用python的'with'语句，但是一定要在建立连接后，及时的断开连接。
    In [3]: mcr = MCRcon("这是一个ip", "这是rcon的密码","这是Rcon的端口" )
    In [4]: mcr.connect() #连接建立
    In [5]: resp = mcr.command("/发送给服务端的指令")
    In [6]: print(resp) #输出
    In [7]: mcr.disconnect() #断开连接
    """
    socket = None

	#重写init方法
    def __init__(self, host, password, port, tlsmode=0):
        self.host = host
        self.password = password
        self.port = port
        self.tlsmode = tlsmode

    def __exit__(self, type, value, tb):
        self.disconnect()
		
    def __enter__(self):
        self.connect()
        return self

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 打开 TLS
        if self.tlsmode > 0:
            ctx = ssl.create_default_context()

            # 禁用主机名和证书验证
            if self.tlsmode > 1:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

            self.socket = ctx.wrap_socket(self.socket, server_hostname=self.host)

        self.socket.connect((self.host, self.port))
        self._send(3, self.password)



    def _read(self, length):
        data = b""
        while len(data) < length:
            data += self.socket.recv(length - len(data))
        return data
		
    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
			
    def _send(self, out_type, out_data):
        if self.socket is None:
            raise MCRconException("发送前必须连接！")

        # 发送请求包
        out_payload = struct.pack('<ii', 0, out_type) + out_data.encode('utf8') + b'\x00\x00'
        out_length = struct.pack('<i', len(out_payload))
        self.socket.send(out_length + out_payload)

        # 读取响应包
        in_data = ""
        while True:
            # 读取数据包
            in_length, = struct.unpack('<i', self._read(4))
            in_payload = self._read(in_length)
            in_id, in_type = struct.unpack('<ii', in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]

            # 异常处理
            if in_padding != b'\x00\x00':
                raise MCRconException("Incorrect padding")
            if in_id == -1:
                raise MCRconException("登录rcon协议失败")

            
            in_data += in_data_partial.decode('utf8')


            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return in_data

    def command(self, command):
        result = self._send(2, command)
        time.sleep(0.003) # MC-72390 （非线程安全的解决办法）
        return result

```