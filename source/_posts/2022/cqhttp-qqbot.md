---
title: 直接使用python做后端连接go-cqhttp的qqbot
date: 2022-12-31 18:53:47
tags:
- python
- QQ机器人
- mySQL
- web
description: 看了go-cqhttp的文档之后，深感我要框架做何用，直接python写个后端和cqhttp用http通讯多简单啊hhh
cover: /img/go-cqhttp.png
categories: 
- 折腾记录
---
## 前言
> 不懂就问，这篇文章的那张图片是go-cqhttp的logo吗

看了go-cqhttp的文档之后，深感我要框架做何用，直接python写个后端和cqhttp用http通讯多简单啊hhh干脆不用nonebot2了
## go-cqhttp配置
首先是go-cqhttp的配置文件修改，需要配置反向http连接的路径和端口
`config.yml`:
```
  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
      #  max-retries: 3         # 最大重试，0 时禁用
      #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
      - url: http://127.0.0.1:8000/ # 地址
      #  secret: ''                  # 密钥
      #  max-retries: 0             # 最大重试，0 时禁用
      #  retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
```

这样接收go-cqhttp的消息只要监听`8000`端口，同时发送请求只需向`5700`端口发送`get`或`post`数据。

## qqbot的python代码实现
不使用nonebot2这样的框架，至少在不算复杂的应用都情况下感觉十分简单
```
import requests
from flask import Flask, request
import pymysql
import time

app = Flask(__name__)

commands = ['记分', '清零', '查询', '复读', 'add', 'del', 'inquire', '12']


def add_score(target, score):
    db = pymysql.connect(host='triority.cn',
                         user='triority',
                         password='xxx',
                         database='qqbot')
    cursor = db.cursor()
    sql = "select score from scores \
            where qq_id = %s" % (target)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) > 0:
        try:
            sql = "update scores set score = score + " + score + " where qq_id = %s" % (target)
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("rollback")
    else:
        try:
            sql = "insert into scores(qq_id, op, score)\
                    values (" + target + ", 0, " + score + ")"
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("rollback")
    sql = "select score from scores where qq_id = %s" % (target)
    cursor.execute(sql)
    results = cursor.fetchall()
    now_score = results[0][0]
    db.close()
    return now_score


def inquire(target):
    try:
        db = pymysql.connect(host='triority.cn',
                             user='triority',
                             password='xxx',
                             database='qqbot')
        cursor = db.cursor()
        sql = "select score from scores where qq_id = %s" % (target)
        cursor.execute(sql)
        results = cursor.fetchall()
        now_score = results[0][0]
        db.close()
    except:
        now_score = '不存在'
    return now_score


def delete(target):
    try:
        db = pymysql.connect(host='triority.cn',
                             user='triority',
                             password='xxx',
                             database='qqbot')
        cursor = db.cursor()
        sql = "select score from scores where qq_id = %s" % (target)
        cursor.execute(sql)
        results = cursor.fetchall()
        now_score = results[0][0]
        sql = "delete from scores where qq_id = %s" % (target)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("rollback")
        del_message = '分数已清零'
        db.close()
    except:
        del_message = '不存在记录'
    return del_message


def private(uid, message):
    if message[0] == '复读':
        requests.get('http://127.0.0.1:5700/send_private_msg?user_id=' + str(uid) +
                     '&message=' + str(message[1]) + '字符串长度' + str(len(message[1])))


def group(gid, uid, message):
    if message[0] == '记分' or message[0] == 'add':
        score = message[1]
        if message[2][0] == '[':
            target = message[2][10:-1]
        else:
            target = message[2]
        new_score = add_score(target, score)
        requests.get(
            'http://127.0.0.1:5700/send_group_msg?group_id=' + str(gid) +
            '&message=' + str(message[2]) + '已增加' + score + '分，当前分数为' + str(new_score))
    elif message[0] == '复读':
        requests.get('http://127.0.0.1:5700/send_group_msg?group_id=' + str(gid) +
                     '&message=' + str(message[1]) + '字符串长度' + str(len(message[1])))
    elif message[0] == '查询' or message[0] == 'inquire':
        if message[1][0] == '[':
            target = message[1][10:-1]
        else:
            target = message[1]
        score = inquire(target)
        requests.get('http://127.0.0.1:5700/send_group_msg?group_id=' + str(gid) +
                     '&message=' + str(message[1]) + '当前分数为' + str(score))
    elif message[0] == '清零' or message[0] == 'del':
        if message[1][0] == '[':
            target = message[1][10:-1]
        else:
            target = message[1]
        del_message = delete(target)
        requests.get('http://127.0.0.1:5700/send_group_msg?group_id=' + str(gid) +
                     '&message=' + str(message[1]) + del_message)


@app.route('/', methods=["POST"])
def post_data():
    print(request.get_json())  # 将原始信息传到后台
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        if message[0] == '/':
            message = message[1:].rstrip().split(' ')
            if message[0] in commands:
                private(uid, message)
    elif request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        if message[0] == '/':
            message = message[1:].rstrip().split(' ')
            if message[0] in commands:
                group(gid, uid, message)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)

```
