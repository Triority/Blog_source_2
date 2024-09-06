---
title: 基于nonebot2+cqhttp的QQ机器人以及使用mySQL的记分系统
date: 2022-12-30 21:24:55
tags:
- python
- QQ机器人
- mySQL
description: 基于nonebot2+cqhttp的QQ机器人以及使用mySQL的记分系统
cover: /img/nonebot.png
categories: 
- 折腾记录
---
## 前言
这篇文章主要讲nonebot的使用，如果内容不多的话整个机器人的制作都写在这吧。
## 记分系统数据库结构
先从简单的讲起。

结构不算复杂，需要一个数据表`scores`，主键为`bigint`类型的QQ号`qq_id`。

表中记录的数据有`int`型的权限级别`op`，`int`型的当前分数`total_score`，`bigint`类型的上一次记分的管理员`last_op`，`int`的上一次的记分`last_score`，`varchar`型都上一次记分的理由`last_reason`，`varchar`型都上一次记分的时间`last_time`。

## 使用nonebot2+cqhttp的插件编写
[有一篇不错的但是不完整的文档](https://github.com/Well2333/NoneBot2_NoobGuide)，文档的作者写一半被nonebot开发者叫去写官方文档了，不过已经写完的这些也有很大帮助。这里我把会用到的整理出来。
[这里还有一些不错的资源汇总](https://github.com/nonebot/awesome-nonebot)
### 插件的位置
`src/plugins`可以在`bot.py`使用 `nonebot.load_plugins("src/plugins")` 来加载该文件夹中的插件。

> 注意！ 如果插件的名字首个字符是 _ 的话，那么这个插件将不会被 “自动加载” ，但仍可以使用单独加载的方式进行载入。

### 插件的结构

##### 模块(module)
  
也就是单文件形式的python脚本，例如下方展示的名为 my_plugin 的插件。
```
NoneBot
├── src
│   └── plugins
|      └── my_plugin.py
|......
```
相对于包形式的插件，模块形式的插件更简单，但相对的只能在一个文件中塞下全部代码
##### 包(package)
以一个文件夹形式存在的包，例如下方展示的名为 my_plugin 的插件。

值得注意的是，在python中，一个合法的包中必须含有一个 __init__.py ，即便其中一个字都没有也不能省略。
```
AweSome-Bot
├── src
│   └── plugins
|      └── my_plugin
|         └── __init__.py
|         └── function.py
|......
```
### 事件响应器与事件处理

一个小例子：
检测用户发送的“jrrp”或“今日人品”，然后随机生成一个1-100的数字作为人品值发回给用户，并@用户
```
import random
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

def luck_simple(num):
    if num < 18:
        return '吉'
    else:
        return '凶'

# 注册事件响应器
jrrp = on_keyword(['jrrp','今日人品'],priority=50)
# 事件处理
@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1,100)
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数为"{luck_simple(lucknum)}"'))
```
因为这个插件需要检测多个关键词，因此我们可以选择 `on_keyword()` 这个事件响应器， `jrrp = on_keyword(['jrrp','今日人品'],priority=50)` 我们就注册好了对这两个关键词进行响应的事件响应器，不过要注意的的是，这个响应器在用户发送的消息中，只要找到了这个关键词就会触发.

其中`priority=50`是指这个事件响应器的优先度为50，优先度的数字越低，则优先度越高，在nonebot中，这个字段的默认值是优先度能设置的最小值`1`。
nonebot的事件处理中有事件阻断机制，在事件向优先度较低的响应器传递的过程中，一旦被匹配到并且被阻断了，那么后续的事件响应器将不会再接收到这个事件。

我们使用了 `event.get_user_id()` 来获取用户的qq号，和 `jrrp.finish()` 来发送消息并结束这个事件。 事件处理的方法有很多，无法一一展示，仅能列出一些常用的方法
##### event
`event.get_message()`
获取用户发送的消息，包含文字和图片的cq码，返回值是Message类（做解析之前别忘了转义）

`event.get_plaintext()`
获取用户发送的消息，但仅包含文字部分，返回值是str类

`event.get_user_id()`
获取用户qq号，返回值是str类

`event.get_session_id()`
私聊：获取用户qq号，返回值是str类 群聊：获取群号和用户qq号的组合，例如 group_群号_qq号 ，返回值是str类

`event.is_tome()`
私聊：返回True，返回值bool类 群聊：如果用户@机器人，或者使用了预设的昵称，则返回True，否则False，返回值bool类

##### matcher
`matcher.send()`
用于发送一条消息，发送的对象是触发事件响应器的私聊或群，用法为:
`await matcher.send('123')`
其中matcher就是这个事件处理函数对应的事件响应器，例如 `await jrrp.send('123')` 

`matcher.finish()`
方法同上，只不过这个方法会结束这个事件，类似于一个函数里的 return （但不完全相同）。

### Message CQ码的基本用法
#### Message
Message不光可以对上述内容进行转义或表达，也可以对其进行拼接，例如
```
from nonebot.adapters.onebot.v11 import Message, MessageSegment
msg1 = Message('快来看涩图')
msg2 = MessageSegment.image('http://xxx.com/')
msg3 = Message('[CQ:at,qq=114514]')
msg  = msg3 + msg1 + msg2

# msg的内容发到QQ里就是：@114514 快来看涩图【假装这是个涩图】
```
#### CQ码
cq码的构造方法一般情况下是 [CQ:type,key=value] 这种构造形式，具体的某个CQ码我们可以在gocqhttp的官方文档的 CQ code 板块进行查询。

同时，由于cq码中存在例如 []、:、= 等符号，因此需要对其进行转义才能够正常使用，方法也很简单，只需要用 Message() 即可转义，例如：
```
from nonebot.adapters.onebot.v11 import Message
raw_cqcode = '[CQ:at,qq=114514]'
cqcode = Message(raw_cqcode)
```
这样就可以是这个CQ码正常的被解析成一个@，而不是直接把CQ码原文发出去了。

### API使用方法
我们使用的[gocqhttp的官方文档](https://docs.go-cqhttp.org/api)中对API有详细的介绍。

call_api的写法目前有两种，`bot.call_api('xxx', **{key:value})`和`bot.xxx(key=value)`两种仅写法不同，实质并无影响。

以“获取群信息”为例进行写法一的演示：
```
from nonebot.adapters.onebot.v11 import Bot
from nonebot import on_message

test = on_command('test')
@test.handle()
async def _(bot: Bot):
    # call_api的写法一
    data = await bot.call_api('get_group_info',**{
        'group_id' : 123456
    })
```
这样我们就获得了data这个json格式的返回值，然后进行简单的转义就可以读取了。 这里我们再演示一下和“发送消息”，并使用第二种方法进行演示。
```
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import on_message
import ast

test = on_command('test')
@test.handle()
async def _(bot: Bot, event: Event):
    # call_api的写法一
    data = await bot.call_api('get_group_info',**{
        'group_id' : 123456
    })
    # 对json进行转义
    data = ast.literal_eval(str(data))
    msg = f"群号  ：{data['group_id']}\
          \n群名称：{data['group_name']}\
          \n成员数：{data['member_count']}"
    # call_api的写法二
    await bot.send(
        event   = event,
        message = msg
    )
    # 不过，这里更推荐直接用响应器的send方法
    # await test.send(msg)
```
### 事件阻断
我们可以通过在事件响应器中添加 `block` 参数来指定该事件响应器是否会在执行完成后进行阻断，也可以在事件处理函数中使用 `matcher.stop_propagation()` 来直接阻断该事件
```
from nonebot import on_message
from nonebot.matcher import Matcher

foo = on_message(priority=1, block=False)
@foo.handle()
async def handle(matcher: Matcher):
    matcher.stop_propagation()
```
### permission
`Permission` 的作用就是对用户身份进行辨认和过滤，仅允许通过判断的用户触发其所属的事件响应器。

| 权限类型  | 匹配范围  |
| ------------ | ------------ |
|PRIVATE|全部私聊|
|PRIVATE_FRIEND|私聊好友|
|PRIVATE_GROUP|群临时私聊|
|PRIVATE_OTHER|其他临时私聊|
|GROUP|全部群聊|
|GROUP_MEMBER|任意群员|
|GROUP_ADMIN|群管理|
|GROUP_OWNER|群主|

只需其中一个返回 `True` 时就会匹配成功

例如，我们想要匹配私聊或群管理时：
```
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN,PRIVATE
from nonebot import on_command

matcher = on_command("setu", permission=PRIVATE|GROUP_ADMIN)
```
这个响应器将会对任意私聊或群聊中的管理员进行响应。

### 事件响应与处理
#### 事件的类型
##### 元事件-metaevent
对应的事件响应器为 `on_metaevent()`

一类特殊的事件，与nonebot2的运行相关，例如心跳事件、ws连接等。 由于该类事件我们一般来说不会做响应，因此我不做过多解释

##### 通知事件-notice
对应的事件响应器为 `on_notice()`

一些较为特殊的事件，且无需管理员的批准即可主动完成的操作，例如上传文件、被禁言、戳一戳这种消息会被归为通知事件。

在nonebot2的运行日志中，通知事件会按照 `[notice.xxx.xxx]: {xxx}` 的形式显现。

其中，`{xxx}`是一个json格式的数据，具体内容可以详见[go-cqhttp的文档](https://docs.go-cqhttp.org/cqcode/)。

##### 请求事件-request
对应的事件响应器为`on_request()`

一些较为特殊的事件，且需要管理员（或你）的批才能完成的操作，例如好友申请、加群申请等。 在nonebot2的运行日志中，请求事件会按照 `[request.xxx]: {xxx}` 的形式显现。

其中，{xxx}是一个json格式的数据，具体内容可以详见[go-cqhttp的文档](https://docs.go-cqhttp.org/cqcode/)。

##### 消息事件-message
对应的事件响应器为 `on_message()`

是最基本的事件，仅通过聊天框和历史记录进行显示的的绝大多数都是消息类型，例如我们日常聊天的内容、发的图片等。 在nonebot2的运行日志中，消息事件会按照`[message.xxx.xxx]: Message xxx from xxx "xxx"`的形式显现。

