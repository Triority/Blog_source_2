---
title: xbox手柄控制
tags:
  - arduino
  - python
  - esp32
  - opencv
cover: /img/QQ截图20230227164056.png
categories:
- 折腾记录
notshow: false
date: 2023-02-27 16:38:34
description: 使用python控制车模
---
## 手柄信息读取
使用python读取xbox手柄数据例程：
![参考链接：https://blog.csdn.net/qq_41556318/article/details/86305263](QQ截图20230227164056.png)
```
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
```
## 上位机远程控制
### 手柄数据获取
使用左侧摇杆作为方向控制，左侧按键作为倒车，右侧为油门(优先级低于左侧)

注意`while`循环里面的`for event in pygame.event.get():`部分不可删除，否则无法读取。
```
import pygame
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():  # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # direction from -1 ~ 1, returns to 0 automatically
    axis0 = joystick.get_axis(0)
    if axis0 > 0.1 or axis0 < -0.1:
        direction = axis0
    else:
        direction = 0
    print(direction)
    # speed from -1 to 1, returns to -1 automatically
    speed = joystick.get_axis(4)
    print(speed)

```
即可得到方向和速度控制数值。
### 使用socket连接传输指令数据
#### 电脑server发送
注意这里用`clock.tick(10)`限制发送速度每秒10次，确保客户端接收速度更快，否则多次发送的json文本将会直接相连被接收，导致无法解析json文本。

```
import time

import pygame
from socket import *
import _thread
import json

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
address = ('127.0.0.1', 7788)


def recv_size(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def web():
    global direction
    global run
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.bind(address)
    tcp_server_socket.listen(8)
    client_socket, client_addr = tcp_server_socket.accept()
    while 1:
        try:
            time.sleep(0.1)
            data = {"direction": direction, "run": run}
            client_socket.send(json.dumps(data).encode('utf-8'))
        except:
            client_socket, client_addr = tcp_server_socket.accept()

_thread.start_new_thread(web, ())


while 1:
    for event in pygame.event.get():  # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # direction from -1 ~ 1, returns to 0 automatically
    axis0 = joystick.get_axis(0)
    if axis0 > 0.1 or axis0 < -0.1:
        direction = axis0
    else:
        direction = 0
    # speed from -1 to 1, returns to -1 automatically
    speed = joystick.get_axis(5) + 1    # 0~2
    speed_back = -1 - joystick.get_axis(4)  # -2~0
    if speed_back == 0:
        run = speed
    else:
        run = speed_back
    print("direction", direction, "run", run, 'speed', speed, 'speed_back', speed_back)
    clock.tick(10)

```
#### 车子client接收
```
import _thread
import re
import time
from socket import *
import json

direction = 0
speed = -1
server = ("127.0.0.1", 7788)


def get_data():
    global direction
    global speed
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(server)
    while 1:
        try:
            rec = s.recv(1024).decode("utf-8")
            data = json.loads(rec)
            direction = float(data['direction'])
            speed = float(data['speed'])
            print("direction", direction, "speed", speed)
        except:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(server)


_thread.start_new_thread(get_data, ())
while 1:
    time.sleep(10)

```
#### client使用ROS控制
将`time.sleep(10)`替换为ROS节点数据发布：
```
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import numpy as np
import _thread
import time
from socket import *
import json

control_speed = 1500  # 500-1499倒车/1500停车/1501-2500前进
turn_mid = 90  # 舵机中值是90
direction = 0
run = 0
server = ("triority.cn", 7788)


def get_data():
    global direction
    global run
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(server)
    while 1:
        try:
            rec = s.recv(1024).decode("utf-8")
            data = json.loads(rec)
            direction = float(data['direction'])
            run = float(data['run'])
            print("direction", direction, "run", run)
        except:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(server)


def publisher(direction, run):
    twist.linear.x = 1500 + int(run * 200)
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 90 - int(direction * 50)
    pub.publish(twist)


_thread.start_new_thread(get_data, ())

if __name__ == "__main__":
    # 声明twist节点
    rospy.init_node('racecar_teleop')
    pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=1)
    twist = Twist()
    # cap = cv2.VideoCapture(0)
    while 1:
        publisher(direction, run)

```
#### 启动命令
使用launch文件启动下位机节点：
```
roslaunch racecar Run_car.launch
```
启动控制python程序：
```
rosrun racecar run_school.py
```
### 图传数据使用opencv低延迟高帧率传输
这个程序有点问题，就是有时候客户端发送图片长度数据之后，服务端接收到无法解析为长度数据，具体原因不清楚，所以直接try然后重建连接了。

最开始延迟很可观，帧率只有5-10，一部分原因是`capture.read()`是一个IO密集型的阻塞函数，把读取和部分编码压缩工作移动到其他线程即可明显改善。
#### 发送图传数据client.py
```
#!/usr/bin/env python3
import socket
import _thread
import cv2
import numpy
import time

# 压缩参数，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
string_data = ''
address = ('triority.cn', 8002)

def read_video():
    global string_data
    capture = cv2.VideoCapture(0)
    while 1:
        ret, read_frame = capture.read()
        # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;用于图像数据格式的压缩，方便网络传输
        result, img_encode = cv2.imencode('.jpg', read_frame, encode_param)
        # 建立矩阵并将numpy矩阵转换成字符形式，以便在网络中传输
        data = numpy.array(img_encode)
        string_data = data.tobytes()


def send_video():
    while 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        while 1:
            time.sleep(0.02)
            try:
                # 先发送要发送的数据的长度 ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
                sock.send(str.encode(str(len(string_data)).ljust(16)))
                sock.send(string_data)
                if cv2.waitKey(10) == 27:
                    break
            except:
                sock.close()
                break


if __name__ == '__main__':
    _thread.start_new_thread(read_video, ())
    time.sleep(5)
    send_video()

```
#### 接受图传数据server.py:
```
import socket
import time
import cv2
import numpy

address = ('127.0.0.1', 8002)


def recv_all(sock, count):
    buf = b''
    while count:
        new_buf = sock.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf


def receive_video():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    while 1:
        conn, addr = s.accept()
        print('connect from:' + str(addr))
        while 1:
            try:
                length = recv_all(conn, 16).decode('utf-8')  # 获得图片文件的长度,16代表获取长度
                string_data = recv_all(conn, int(length))  # 根据获得的文件长度，获取图片文件
                data = numpy.frombuffer(string_data, numpy.uint8)  # 将获取到的字符流数据转换成数组
                dec_img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
                cv2.imshow('SERVER', dec_img)
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
            except:
                conn.close()
                break

if __name__ == '__main__':
    receive_video()

```
## 香橙派与arduino串口通信(失败)
### arduino接收串口数据控制电调舵机
电调的有效值是`1000-2000`的脉宽，舵机直接使用角度控制有效值`60-120`。将两者相接一起串口发送到arduino下位机。
如`1800090`表示速度`1800`,角度`90`.
```
#include <Servo.h>

Servo myServo;
Servo pwm;

String comStr = "";
long comInt=0;
long speed=2000;
long dir=90;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(Serial.read()>=0){} // clear serial port's buffer
  
  myServo.attach(9); // attach myServo to GPIO_09
  myServo.write(90);
  pwm.attach(10);

  pwm.writeMicroseconds(2000);
  delay(1500);
  pwm.writeMicroseconds(1500);
  delay(1500);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    // listen the Serial port, run the code when something catched..
    delay(30);
    comStr = Serial.readString();
    comInt = comStr.toInt();
    comInt = constrain(comInt, 1000060, 2000120);
    Serial.println(comStr);
    Serial.println(comInt);
    speed = comInt/1000;
    speed = constrain(speed, 1000, 2000);
    Serial.println(speed);
    dir = comInt - speed*1000;
    dir = constrain(dir, 60, 120);
    Serial.println(dir);

    myServo.write(dir);
    pwm.writeMicroseconds(speed);
    
  }
  
}

```
### 香橙派串口数据通信(失败)

```
import serial
import serial.tools.list_ports

ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备")
else:
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
ser.write('1500090'.encode())
```
发送后arduino串口灯有闪烁，但是没有反应，显然没有正确传输信息。

## 使用esp32直接接收服务器命令
舵机库无法在esp32上运行，但是esp32输出pwm控制比arduino方便得多hhh

现在真的是觉得esp32比arduino好用太多了，以后有空写个esp32的教程合集吧。

### esp32连接wifi并接收tcp数据以及PWM输出
```
#include <WiFi.h>

const char *ssid = "Triority3434";
const char *password = "123654789";

const IPAddress serverIP(47,243,172,141);
uint16_t serverPort = 7788;
WiFiClient client;

int freq = 50;
int freq2 = 500;
int channel = 8;    // 通道(高速通道（0 ~ 7）由80MHz时钟驱动，低速通道（8 ~ 15）由 1MHz 时钟驱动。)
int channel2 = 15;
int resolution = 8; // 分辨率
const int servo = 12;
const int pwm = 13;

int dir = 90;
int run = 1500;

int servoPWM(int degree)
{ // 0-180度
  // 20ms周期，高电平0.5-2.5ms，对应0-180度角度
  const float deadZone = 6.4;//对应0.5ms（0.5ms/(20ms/256）)
  const float max = 32;//对应2.5ms
  if (degree < 60)
    degree = 60;
  if (degree > 120)
    degree = 120;
  return (int)(((max - deadZone) / 180) * degree + deadZone);
}

void setup(){
  Serial.begin(9600);
  Serial.println();
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.setHostname("esp32-car");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(2000);
    Serial.print(".");
  }
  Serial.println("WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());
  
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(servo, channel);

  ledcSetup(channel2, freq2, resolution);
  ledcAttachPin(pwm, channel2);

  ledcWrite(channel, servoPWM(90));
  delay(500);
  ledcWrite(channel2, 255);
  delay(1500);
  ledcWrite(channel2, 191);
  delay(1500);
}

void loop(){
  Serial.println("connecting to server");
  if (client.connect(serverIP, serverPort)){
    Serial.println("connected");
    while (client.connected() || client.available()){
      if (client.available()){
        String d = client.readStringUntil('d');
        Serial.println(d);
        dir = d.toInt();
        String r = client.readStringUntil('r');
        run = r.toInt();
        Serial.println(r);

        ledcWrite(channel, servoPWM(dir));
        ledcWrite(channel2, int(run*256/2000-1));
      }
    }
  }else{
    Serial.println("err");
    client.stop();
  }
  delay(5000);
}

```
#### 以及进行了轻微修改的控制程序
```
import time

import pygame
from socket import *
import _thread
import json

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
address = ('127.0.0.1', 7788)


def recv_size(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def web():
    global direction
    global run
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.bind(address)
    tcp_server_socket.listen(8)
    client_socket, client_addr = tcp_server_socket.accept()
    while 1:
        try:
            time.sleep(0.03)
            dir = 90 - int(direction*30)
            if run >= 0:
                r = 1500 + int(250*run)
            else:
                r = 1100
            client_socket.send((str(dir)+'d'+str(r)+'r').encode('utf-8'))
        except:
            client_socket, client_addr = tcp_server_socket.accept()

_thread.start_new_thread(web, ())


while 1:
    for event in pygame.event.get():  # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # direction from -1 ~ 1, returns to 0 automatically
    axis0 = joystick.get_axis(0)
    if axis0 > 0.1 or axis0 < -0.1:
        direction = axis0
    else:
        direction = 0
    # speed from -1 to 1, returns to -1 automatically
    speed = joystick.get_axis(5) + 1    # 0~2
    speed_back = -1 - joystick.get_axis(4)  # -2~0
    if speed_back == 0:
        run = speed
    else:
        run = speed_back
    print("direction", direction, "run", run, 'speed', speed, 'speed_back', speed_back)
    clock.tick(10)

```
## RUN！

{% dplayer "url=https://cr.triority.cn/f/95Lum/car_school.mp4" %}