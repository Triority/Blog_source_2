---
title: 用python写个聊天室
tags:
  - python
cover: /img/aboutqqbot.png
categories:
- 折腾记录
notshow: false
date: 2023-01-24 13:40:42
description: 别问，问就是闲的
---
## 别问，问就是闲的
python用了一年半了，我说这是我第一次自己写class你信吗hhh

当然写这个主要是因为这里面包括了很多以后可能需要的东西，比如多线程socket连接，以及后面的改进内容里的线程锁等等等，里面也有一些无关紧要的东西比如base64”加密“，反正很简单加进去就完了hhh也许将来无聊直接给他写成https加密呢，那样加密就不用带引号了
## 程序
### 服务端
```
import socket
import sys
import threading
import time
import json
import base64


class ChatSever:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ("0.0.0.0", 12345)
        self.users = {}
        self.rooms = {}

    def start_sever(self):
        try:
            self.sock.bind(self.addr)
        except Exception as e:
            print(e)
        self.sock.listen(1024)
        print("服务器已开启，等待连接...")
        self.accept_cont()

    def accept_cont(self):
        while True:
            s, addr = self.sock.accept()
            client_note = json.loads(base64.b64decode(s.recv(1024)).decode("gbk"))
            room_id = client_note["room_id"]
            name = client_note["name"]
            self.users[addr] = [s, room_id, name]
            if room_id in self.rooms:
                self.rooms[room_id].append(name)
            else:
                self.rooms[room_id] = [name]
            print("{}连接成功，{}已加入房间{}，其中有{}位用户:{}，当前连接的用户共有{}".format(addr, name, room_id, len(self.rooms[room_id])
                                                                    , self.rooms[room_id], len(self.users)))
            threading.Thread(target=self.recv_send, args=(s, addr, name, room_id)).start()

    def recv_send(self, sock, addr, name, room_id):
        sock.send(base64.b64encode("您已成功加入房间{}，当前房间内有{}位用户：{}".format(room_id, len(self.rooms[room_id])
                                                                      , self.rooms[room_id]).encode('gbk')))
        for client in self.users.values():
            if client[1] == room_id:
                client[0].send(
                    base64.b64encode("{}：用户{}加入了聊天室。".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                             , name).encode("gbk")))
        while True:
            try:
                response = base64.b64decode(sock.recv(4096)).decode("gbk")
                for client in self.users.values():
                    if client[1] == room_id:
                        msg = "{}：用户{}发送消息：{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                      , name, response)
                        client[0].send(base64.b64encode(msg.encode("gbk")))
            except ConnectionResetError:
                print("{}房间的{}用户{}已经退出聊天!".format(room_id, addr, name))
                self.users.pop(addr)
                self.rooms[room_id].remove(name)
                for client in self.users.values():
                    if client[1] == room_id:
                        client[0].send(base64.b64encode(
                            "{}：用户{}已经退出聊天!".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                    , name).encode("gbk")))
                break

    def close_sever(self):
        for client in self.users.values():
            client.close()
        self.sock.close()
        sys.exit()


if __name__ == "__main__":
    sever = ChatSever()
    sever.start_sever()
    while True:
        cmd = input()
        if cmd == "stop":
            print("正在关闭...")
            sever.close_sever()
        else:
            pass

```
### 客户端
```
import base64
import socket
import sys
import threading
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("triority.cc", 12345)
room_id = input("请输入房间号：")
name = input("请输入你的昵称：")
client = {"room_id": room_id, "name": name}
s.connect(addr)
s.send(base64.b64encode(json.dumps(client).encode("gbk")))


def recv_msg():
    print("连接成功！现在可以接收消息！\n")
    while True:
        try:
            response = base64.b64decode(s.recv(4096)).decode("gbk")
            print(response)
        except ConnectionResetError:
            print("服务器关闭，聊天已结束！")
            s.close()
            break
    sys.exit()


def send_msg():
    print("连接成功！现在可以发送消息！\n")
    print("窗口底部输入消息后按回车发送")
    print("发送esc退出聊天")
    while True:
        msg = input()
        if msg == "esc":
            print("你退出了聊天")
            s.close()
            break
        s.send(base64.b64encode(msg.encode("gbk")))
    sys.exit()


threads = [threading.Thread(target=recv_msg), threading.Thread(target=send_msg)]
for t in threads:
    t.start()

```

## 改进
上面的已经可以实现我想要的功能了，但是要改进的话，显而易见的以后也有可能再写个GUI吧，不过那是以后的事，现在想的是加一个log功能，服务端保存登入登出记录的数据，由于每个与客户端的连接都在不同线程，这就涉及到了多线程对同一文件同时修改的问题，也就需要线程锁来保证同一时间只有一个线程在读写文件
### 线程锁
#### 多线程的冲突
由于线程之间的全局变量是共享的，因此在多线程访问的时候可以会有一些问题：
```
import threading
a = 0

def do_thread1():
    global a
    for i in range(1000000):
        a += 1
 
def do_thread2():
    global a
    for i in range(1000000):
        a += 1
 
if __name__ == '__main__':
    print('---------main begin ----------')
    t1 = threading.Thread(target=do_thread1)
    t2 = threading.Thread(target=do_thread2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(a)
    print('---------main end ----------')

```
理论上说结果应该是`2000000`，但是实际上由于可能一个线程取出a还没增加时另一个线程执行了a增加操作，就会浪费一次运算次数，所以实际输出不一定是多少，比如我这一次：
```
---------main begin ----------
1724297
---------main end ----------

Process finished with exit code 0
```
#### 访问共同资源的时候加锁
```
import threading
a = 0


def do_thread1():
    global a
    for i in range(1000000):
        mutex.acquire()
        a += 1
        mutex.release()


def do_thread2():
    global a
    for i in range(1000000):
        mutex.acquire()  # 加锁
        a += 1
        mutex.release()  # 解锁


if __name__ == '__main__':
    print('---------main begin ----------')
    mutex = threading.Lock()  # 创建一把锁
    t1 = threading.Thread(target=do_thread1)
    t2 = threading.Thread(target=do_thread2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(a)
    print('---------main end ----------')

```
先使用`threading.Lock()`方法获得一个锁，默认是没上锁的状态，当两个线程开始执行后，开始同时竞争这一把锁。那个线程先获得到锁哪个线程就可以继续执行，获得不到锁的线程只能在原地阻塞等待释放锁。这样就保证了同一时刻只能有一个线程访问全局变量，某段关键代码只能由一个线程从头到尾完整地执行。

这一次输出是正确的：
```
---------main begin ----------
2000000
---------main end ----------

Process finished with exit code 0
```
### 带有log的服务端
回到我们的服务端程序，在log记录的线程里，先加锁，再读写文件，再开锁，避免文件写入混乱。
```
import socket
import sys
import threading
import time
import json
import base64


class ChatSever:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ("0.0.0.0", 12345)
        self.users = {}
        self.rooms = {}

    def start_sever(self):
        try:
            self.sock.bind(self.addr)
        except Exception as e:
            print(e)
        self.sock.listen(1024)
        print("服务器已开启，等待连接...")
        self.accept_cont()

    def accept_cont(self):
        mutex = threading.Lock()
        while True:
            s, addr = self.sock.accept()
            client_note = json.loads(base64.b64decode(s.recv(1024)).decode("gbk"))
            room_id = client_note["room_id"]
            name = client_note["name"]
            self.users[addr] = [s, room_id, name]
            if room_id in self.rooms:
                self.rooms[room_id].append(name)
            else:
                self.rooms[room_id] = [name]
            print("{}连接成功，{}已加入房间{}，其中有{}位用户:{}，服务端当前连接的用户共有{}位".format(addr
                                                                        , name, room_id, len(self.rooms[room_id])
                                                                        , self.rooms[room_id], len(self.users)))
            threading.Thread(target=self.recv_send, args=(s, addr, name, room_id, mutex)).start()

    def recv_send(self, sock, addr, name, room_id, mutex):
        sock.send(base64.b64encode("您已成功加入房间{}，当前房间内有{}位用户：{}".format(room_id, len(self.rooms[room_id])
                                                                      , self.rooms[room_id]).encode('gbk')))
        mutex.acquire()
        log_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '：总人数：' + str(len(self.users)) + str(
            addr) + '以昵称' + name + '加入了房间' + room_id
        f = open('log.txt', 'a', encoding="utf-8")
        f.write(log_str + '\n')
        f.close()
        mutex.release()
        for client in self.users.values():
            if client[1] == room_id:
                client[0].send(
                    base64.b64encode("{}：用户{}加入了聊天室。".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                             , name).encode("gbk")))
        while True:
            try:
                response = base64.b64decode(sock.recv(4096)).decode("gbk")
                for client in self.users.values():
                    if client[1] == room_id:
                        msg = "{}：用户{}发送消息：{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                      , name, response)
                        client[0].send(base64.b64encode(msg.encode("gbk")))
            except ConnectionResetError:
                print("{}房间的{}用户{}已经退出聊天!".format(room_id, addr, name))
                self.users.pop(addr)
                self.rooms[room_id].remove(name)
                mutex.acquire()
                log_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '：总人数：' + str(len(self.users)) + str(
                    addr) + '昵称' + name + '退出了房间' + room_id
                f = open('log.txt', 'a', encoding="utf-8")
                f.write(log_str + '\n')
                f.close()
                mutex.release()
                for client in self.users.values():
                    if client[1] == room_id:
                        client[0].send(base64.b64encode(
                            "{}：用户{}已经退出聊天!".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                    , name).encode("gbk")))
                break

    def close_sever(self):
        for client in self.users.values():
            client.close()
        self.sock.close()
        sys.exit()


if __name__ == "__main__":
    sever = ChatSever()
    sever.start_sever()
    while True:
        cmd = input()
        if cmd == "stop":
            print("正在关闭...")
            sever.close_sever()
        else:
            pass

```
这样得以实现人数的记录

### 扫端口
哦突然想起来，以前就有的，经常有人对所有端口各种扫描，会导致无法解析json报错然后程序停止运行，很好解决，给这一段加上，如果无法解析就`continue`。
```
            room_id = client_note["room_id"]
            name = client_note["name"]
```
这一部分改成：
```
            try:
                room_id = client_note["room_id"]
                name = client_note["name"]
            except KeyError:
                s.send('fuck u'.encode('utf-8'))
                s.close()
                print('Error client from ' + addr)
                continue
```
### 使用pyqt5带有GUI的客户端
用Qt Designer设计了一个(十分丑陋的)GUI界面。在做的时候遇到一个问题，就是说当GUI窗口关闭之后，获取新消息的子线程仍在工作。原因是主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束，显然我们的子线程任务是一个死循环。

解决方法是将线程设置为一个守护线程，主线程退出时子线程也会被强制关闭。
```
t = threading.Thread(target=recv_msg)
t.setDaemon(True)
```
这样只要关闭GUI窗口，`recv_msg`函数的线程也会被关闭。

```
pyinstaller -F -w -i LOGO.ico -n PyQt5_SecretChat pyqt5_client.py
```
全部客户端代码：
```
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import base64
import socket
import threading
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("triority.cc", 12345)


def recv_msg():
    print("消息接收线程已启动")
    while True:
        try:
            response = base64.b64decode(s.recv(4096)).decode("gbk")
            Ui_MainWindow.string_add(ui, response)
        except ConnectionResetError:
            Ui_MainWindow.string_add(ui, "服务器关闭，聊天室已关闭！")
            s.close()
            break
    print("消息接收线程已关闭")


class Ui_MainWindow(object):

    def __init__(self):
        self.t = threading.Thread(target=recv_msg)
        self.t.setDaemon(True)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 857)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 1101, 811))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setMaxLength(512)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setMaxLength(512)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.connect_room)
        self.pushButton_2.clicked.connect(self.send)
        self.lineEdit_3.textChanged.connect(self.text_changed)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SecretChat"))
        self.lineEdit_2.setText(_translate("MainWindow", "请在此输入你们的房间号"))
        self.lineEdit.setText(_translate("MainWindow", "请在此输入你想使用的昵称"))
        self.pushButton.setText(_translate("MainWindow", "进入聊天室"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", "发送消息"))

    def connect_room(self):
        name = self.lineEdit.text()
        room_id = self.lineEdit_2.text()
        client = {"room_id": room_id, "name": name}
        s.connect(addr)
        s.send(base64.b64encode(json.dumps(client).encode("gbk")))
        self.pushButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.t.start()
        self.string_add('正在加入聊天室：'+room_id+'...')

    def send(self):
        text = self.lineEdit_3.text()
        s.send(base64.b64encode(text.encode("gbk")))
        self.lineEdit_3.setText('')

    def string_add(self, message):
        string = self.label.text()
        if string.count('\n') > 40:
            ind1 = string.find('\n')
            string = string[ind1 + 1:]
        string += message + '\n'
        self.label.setText(string)

    def text_changed(self):
        msg = self.lineEdit_3.text()
        if '=' in msg:
            msg = msg.replace('=', '')
            self.lineEdit_3.setText(msg)
            self.send()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
```
