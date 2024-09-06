---
title: 使用esp32远程web控制
date: 2022-11-12 02:03:25
tags:
- python
- web
description: esp32连接web服务器获取命令实现远程控制
cover: /img/auto-access.jpg
categories: 
- [折腾记录]
- [作品&项目总结]
- [值得一提的文章]
---
## 前言
最近需要做一个远程控制的门禁，最好可以公网连接[所以下面的server.py在公网服务器运行]，还要有权限管理，和进入行为记录。所以。。。
## 代码
### 服务器
#### python
这个是在公网服务器上运行的程序，使用flask框架创建web网页服务，接收到提交的数据之后通过全局变量，使面向esp32连接的服务端发送指定数据实现远程开门。
`server.py`
```python
import time
from flask import Flask, request, redirect, render_template, session
import _thread
import socket
import json

access = 0

app = Flask(__name__)

app.secret_key = 'QWERTYUIOP'  # 对用户信息加密


def socket_server(x):
    global access
    print('新线程已开启')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('0.0.0.0', xxx))
    s.listen()
    while (True):
        try:
            c, addr = s.accept()
            print('收到连接：'+str(addr))
            if access == 1:
                print('门禁已开启')
                c.send('1'.encode('utf-8'))
                access = 0
            else:
                c.send('0'.encode('utf-8'))
            c.close()
        except Exception as e:
            print(e)


@app.route('/', methods=['GET', "POST"])
def login():
    global access
    d = open("dictionary.txt", "r")
    json_dictionary = d.read()
    d.close()
    dictionary = json.loads(json_dictionary)
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    reason = request.form.get('reason')
    time.sleep(1)
    if reason=='':
        return render_template('login.html', msg='事由不能为空')
    if user in dictionary and pwd == dictionary[user]:
        session['user_info'] = user
        access = 1
        f = open("note.txt", "a")
        f.write("时间:"+str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+",姓名："+user+",事由："+reason+"\n")
        f.close()
        print('用户'+user+'已登录')
        return redirect('/index')
    else:
        return render_template('login.html', msg='姓名或密码输入错误')


@app.route('/index')
def index():
    global access
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return 'The door is opened now! Welcome!'


@app.route('/logout')
def logout_():
    del session['user_info']
    return redirect('login')


if __name__ == "__main__":
    _thread.start_new_thread(socket_server, (0,))
    app.run(host='0.0.0.0', port=5000, debug=False)

```
#### html
在`templates/`路径创建html文件：
`login.html`
```html
<!DOCTYPE html>
 <html>
 <head>
     <meta  charset="UTF-8">
     <title>门禁权限申请</title>
 </head>
 <body>
     <h1>提交申请信息</h1>
     <form  method="post">
         <h3>学号</h3>
         <input type="text"  name="user" >
         <h3>密码</h3>
         <input  type="password" name="pwd" >
         <h3>事由</h3>
         <input  type="text" name="reason" >
         <input  type="submit" name="登录">{{msg}}
     </form>
 </body>
 </html>
```
同时创建空白的`note.txt`文件，用于记录，记录不会被删除，每次新的记录都会被追加在末尾。
### esp32单片机
#### micro python
第一次实操micro python，感觉很棒hhh
`boot.py`
```python
import network as n
import socket
import time
ssid="xxx" #WiFi名
passwd="xxx" #WiFi密码
host="xxx" #服务器IP地址
port=xxx #服务器端口
wlan=None
s=None
try:
    wlan=n.WLAN(n.STA_IF)
    print("开始连接WIFI")
    wlan.active(True)
    #关闭连接，确保没有任何连接，以免失败
    wlan.disconnect()
    wlan.connect(ssid,passwd)
    #确保WiFi连接成功
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
    print("连接WIFI完成")
    while True:
        #建立socket连接
        s = socket.socket()
        #Socket属性
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #连接服务器
        s.connect((host,port))
        #发送数据
        #print("TCP Connected to:", host, ":", port)
        data = s.recv(1024).decode('utf-8')
        #print(data)
        if data=='1':
            print('开门')
        s.close()
        time.sleep(1)
except Exception as e:
    print(e)
```
#### c
```c
#include<WiFi.h>
const char* id="xxx";   //定义两个字符串指针常量
const char* psw="xxx";
const IPAddress serverIP(x,x,x,x);
uint16_t serverPort = xxx;
WiFiClient client;
int freq = 50;      // 频率(20ms周期)
int channel = 8;    // 通道(高速通道（0 ~ 7）由80MHz时钟驱动，低速通道（8 ~ 15）由 1MHz 时钟驱动。)
int resolution = 8; // 分辨率
const int led = 13;


int calculatePWM(int degree){
  //20ms周期，高电平0.5-2.5ms，对应0-180度角度
  const float deadZone = 6.4;//对应0.5ms（0.5ms/(20ms/256）)
  const float max = 32;//对应2.5ms
  if (degree < 0)
    degree = 0;
  if (degree > 180)
    degree = 180;
  return (int)(((max - deadZone) / 180) * degree + deadZone);
}


void setup() {
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(led, channel);
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(id,psw);
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.println("正在连接...");
  }
  Serial.println("连接成功！");
  Serial.print("IP Address:");
  Serial.println(WiFi.localIP());
  ledcWrite(channel, calculatePWM(0));
}

void loop()
{
    Serial.println("尝试访问服务器");
    if (client.connect(serverIP, serverPort)){
        Serial.println("访问成功");
        while (client.connected() || client.available())
        {
            if (client.available()) //如果有数据可读取
            {
                //String line = client.readStringUntil('\n'); //读取数据到换行符
                String line = client.readString();
                Serial.print("读取到数据：");
                Serial.println(line);
                if (line.indexOf('1')!=-1){
                  Serial.println("开门");
                  ledcWrite(channel, calculatePWM(180));
                  }else{
                    ledcWrite(channel, calculatePWM(0));
                    }
            }
        }
        //Serial.println("关闭当前连接");
        client.stop(); //关闭客户端
    }
    else
    {
        //Serial.println("访问失败");
        client.stop(); //关闭客户端
    }
    delay(500);
}
```