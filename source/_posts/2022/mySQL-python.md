---
title: mySQL数据库的基本操作以及使用python连接数据库
date: 2022-12-30 15:35:43
tags:
- python
- QQ机器人
- 笔记
- mySQL
description: 以制作一个QQ机器人记分系统为主要任务，记录数据库学习过程
cover: /img/mySQL.png
categories: 
- 文档&笔记
---
## 前言
之前曾经写过一个QQ机器人的插件，能够对成员进行记分操作，如果记分达到一定数量将会提醒管理，把这个多次违规的成员t掉。那时候使用的方法是json记录数据，然后转换成npy的格式保存。但是随着数据越来越多，json已经无法满足需要，而且也打算借此机会学习一下数据库的使用。这篇文章将会以QQ机器人记分系统为主要任务，记录我的学习过程。
## 准备工作
因为是共用的记分记录，因此把数据库部署在了服务器上，这部分就有宝塔面板来完成了。安装了mySQL，然后新建了一个名称为`qqbot`的数据库，管理员账号为`triority`，允许公网访问。
## 使用python连接数据库并进行基本操作
### pymysql库的安装
首先安装`pymysql`
```
python -m pip install pymysql
```
### 建立连接访问数据库和断开连接
```
db = pymysql.connect(host='triority.cn',
                     user='triority',
                     password='xxx',
                     database='qqbot')
```
于是我们与数据库建立了连接，可以访问其中的数据。
```
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print("Database version : %s " % data)
```
输出为`Database version : 5.5.62-log`
```
# 关闭数据库连接
db.close()
```
### 创建表
如果数据库连接存在我们可以使用`execute()`方法来为数据库创建表
```
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("drop table if exists scores")

# 使用预处理语句创建表，包括同时作为主键的QQ号，当前分数，上一次记分的管理员，上一次记分时间以及理由
sql = """create table scores (
         qq_id  int primary key,
         score int,
         last_op int,
         last_time char(64),
         last_reason char(64) not null default '' )"""
cursor.execute(sql)

# 关闭数据库连接
db.close()
```
### 插入数据
```
cursor = db.cursor()

# SQL 插入语句
sql = """insert into scores(qq_id,
         score, last_op, last_time, last_reason)
         values (2605925210, 5, 2605925210, '2022.12.30', 'test')"""
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()

# 关闭数据库连接
db.close()
```
### 查询数据
这里我们查询所有分数大于3的成员，刚才已经提交了信息，`2605925210`的分数为5，因此应该能被搜索到
```
cursor = db.cursor()

# SQL 查询语句
sql = "select * from scores \
       where score > %s" % (3)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        qq_id = row[0]
        score = row[1]
        last_op = row[2]
        last_time = row[3]
        last_reason = row[4]
        # 打印结果
        print("qq_id=%s,score=%s,last_op=%s,last_time=%s,last_reason=%s" % \
              (qq_id, score, last_op, last_time, last_reason))
except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()
```
输出内容如下
```
qq_id=2147483647,score=5,last_op=2147483647,last_time=2022.12.30,last_reason=test
```
显然QQ号是错误的，但是其他信息正确，原因在于建表时使用了`int`型数据，最大值为`2147483647`，而我的QQ号超过了这一数值，因此被设置为最大值。也幸好，如果我的QQ号首位是1，我就不会发现这个致命bug。

我的解决方法当然就是重新建表，不知道学到后面会不会有直接改表数据类型的方法hhh

这里就重新建表，把`qq_id`的类型改为`bigint`这肯定够长了hhh

这次建表`sql`改为
```
sql = """create table scores (
         qq_id  bigint primary key,
         score int,
         last_op bigint,
         last_time varchar(64),
         last_reason varchar(64) not null default '' )"""
```

输出正确：
```
qq_id=2605925210,score=5,last_op=2605925210,last_time=2022.12.30,last_reason=test
```

### mySQL数据类型
这里顺便补充一下各种类型的长度：

|MySQL数据类型 | 长度| 范围 |
| :----- | :--: | -------: |
|tinyint | 1个字节 | -128~127|
|smallint | 2个字节 | -32768~32767|
|mediumint | 3个字节 | -8388608~8388607|
|int | 4个字节 | -2147483648~2147483647|
|bigint | 8个字节 | +-9.22*10的18次方|
|float(m,d)| 8位精度(4字节)|m总个数，d小数位|
|double(m,d)|16位精度(8字节)|m总个数，d小数位|

对于浮点数，在数据库中存放的是近似值：

`float(5,3)` 如果插入一个数`123.45678`,实际数据库里存的是`123.457`，但总个数还以实际为准，即6位。

定点类型在数据库中存放的是精确值：

`decimal(m,d)` 参数m<65 是总个数，d<30且 d<m 是小数位

对于字符串：

`char(n)`	固定长度，最多255个字符

`varchar(n)`	可变长度，最多65535个字节

`tinytext`	可变长度，最多255个字符

`text`	可变长度，最多65535个字符

`mediumtext`	可变长度，最多2的24次方-1个字符

`longtext`	可变长度，最多2的32次方-1个字符

### 更新操作
更新操作用于更新数据表的数据，以下将表中`score`大于 `3` 的 `last_op` 字段递增 1：
```
cursor = db.cursor()

# SQL 更新语句
sql = "update scores set last_op = last_op + 1 where score > '%c'" % (3)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()
```
再查询一次，`last_op`已经增加到了`2605925211`：
```
qq_id=2605925210,score=5,last_op=2605925211,last_time=2022.12.30,last_reason=test
```
### 删除操作
删除数据表 `scores` 中 `score` 大于 `12` 的所有数据：
```
# SQL 删除语句
sql = "delete from scores where score > %s" % (12)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交修改
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()
```
### 执行事务
Python DB API 2.0 的事务提供了两个方法 `commit` 或 `rollback`。
事务机制可以确保数据一致性。

事务应该具有4个属性：原子性、一致性、隔离性、持久性。
- 原子性（atomicity）。一个事务是一个不可分割的工作单位，事务中包括的诸操作要么都做，要么都不做。
- 一致性（consistency）。事务必须是使数据库从一个一致性状态变到另一个一致性状态。一致性与原子性是密切相关的。
- 隔离性（isolation）。一个事务的执行不能被其他事务干扰。即一个事务内部的操作及使用的数据对并发的其他事务是隔离的，并发执行的各个事务之间不能互相干扰。
- 持久性（durability）。持续性也称永久性（permanence），指一个事务一旦提交，它对数据库中数据的改变就应该是永久性的。接下来的其他操作或故障不应该对其有任何影响。
```
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 向数据库提交
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()
```
## mySQL基础操作
其实上面的东西已经足够去写这个机器人了，这里就当留一个坑，如果更深入地学了mySQL就来继续写。不过话说回来为什么网上的教程都是大写的SQL命令，单词全都不认识了hhh查过了命令大小写是等价的，而且在windows系统下甚至不分大小写。反正我是用小写了，为了`翻译`网上的教程甚至写了这个，乐
```
string = '''

'''
print(string.lower())
```
