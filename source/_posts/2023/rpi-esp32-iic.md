---
title: 树莓派和esp32电机控制器通讯的底盘控制
tags:
  - esp32
  - arduino
  - 树莓派
cover: /img/Rpi4b.jpg
categories:
- 折腾记录
date: 2023-07-10 14:02:29
description: 树莓派与esp32通讯来控制电机转速，并据此计算小车底盘的位置信息
---
# 上下位机通讯
## iic
在[这篇文章](https://triority.cc/2023/esp32-all-in-one/#%E5%BA%94%E7%AD%94%E4%BA%A4%E4%BA%92%E9%80%9A%E8%AE%AF)我已经写过arduino uno和esp32通讯并控制电机速度，但是树莓派并没有封装好的Wire库，或者说我没找到，所以如果使用树莓派作为上位机这段程序需要重写。

> 树莓派速度发送程序（还没有进行位置计算）:
```
import time
import numpy as np
from smbus2 import SMBus
i2c = SMBus(1)
i2c.open(1)
while 1:
  inf = "0010!"
  adr = 0x08
  str_list = np.fromstring(inf,dtype=np.uint8)

  str_list=np.append(str_list,10)
  for i in str_list:
      #print(i)
      i = int(i)
      i2c.write_byte(adr,i,force=None)
  time.sleep(0.1)
```

> esp32电机控制程序：
```
#include <SimpleFOC.h>
#include <Wire.h>
#include <dummy.h>

MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(25, 26, 27, 14);

float target_velocity = 0;

TwoWire Wire_foc = TwoWire(0);
TwoWire Wire_rec = TwoWire(1);

String inString="";

void setup() {
  Serial.begin(115200);

  Wire_rec.setPins(16,17);
  Wire_rec.begin(0x08);
  Wire_rec.onReceive(receiveEvent);
  Wire_rec.onRequest(requestEvent);

  Wire_foc.setPins(33,32);
  Wire_foc.begin();
  sensor.init(&Wire_foc);

  motor.linkSensor(&sensor);

  driver.voltage_power_supply = 12;
  driver.init();

  motor.linkDriver(&driver);

  motor.controller = MotionControlType::velocity;

  motor.PID_velocity.P = 0.2f;
  motor.PID_velocity.I = 20;
  motor.PID_velocity.D = 0;
  motor.voltage_limit = 6;
  motor.PID_velocity.output_ramp = 1000;
  motor.LPF_velocity.Tf = 0.01f;

  motor.init();
  motor.initFOC();

  _delay(1000);
}

void loop() {
  motor.loopFOC();

  motor.move(target_velocity);
}

void receiveEvent(int howMany) {
    target_velocity = inString.toFloat()/100;
    char ch = Wire_rec.read();
    inString += ch;
    if (ch=='!'){
      inString[4]=0;
      target_velocity = inString.toFloat()/100;
      Serial.println(target_velocity);
      inString="";
    }
}

void requestEvent() {
  float get_ang = sensor.getAngle();
  int ang = int(get_ang*100);
  Serial.println(ang);
  char cstr[8];
  itoa(ang, cstr, 10);
  Wire_rec.write(cstr);
}

```
## 串口
使用iic出现的问题就是电机抖动，iic读取和发送的时间太长了影响了电机运算，所以改用了串口。实际上串口也会有卡顿现象，随着角度数量级增加卡顿更加明显，因此进行了降采样。实测3倍降采样在-104rad范围内工作完美。
> esp32接收速度并发送编码器累计里程
```
#include <SimpleFOC.h>

MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);
BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(25, 26, 27, 14);

float target_velocity = 0;

int i = 0;

Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&target_velocity, cmd); }

void setup() {
  Wire.setPins(33,32);
  Wire.begin();
  sensor.init(&Wire);
  motor.linkSensor(&sensor);

  driver.voltage_power_supply = 12;
  driver.init();
  motor.linkDriver(&driver);

  motor.controller = MotionControlType::velocity;
  motor.PID_velocity.P = 0.2f;
  motor.PID_velocity.I = 20;
  motor.PID_velocity.D = 0;
  motor.voltage_limit = 6;
  motor.PID_velocity.output_ramp = 1000;

  motor.LPF_velocity.Tf = 0.01f;

  Serial.begin(115200);
  motor.useMonitoring(Serial);
  motor.init();
  motor.initFOC(4.53, Direction::CCW);

  command.add('T', doTarget, "target velocity");
  _delay(1000);
}

void loop() {
  motor.loopFOC();
  motor.move(target_velocity);
  command.run();
  i++;
  if(i%3==0) {
    //Serial.print(sensor.getVelocity());
    //Serial.print("---");
    Serial.println(sensor.getAngle());
  }
}

```

> 树莓派使用python发送速度接收里程

记得获取usb设备和读写权限
```
ls /dev/ttyUSB*
sudo chmod 777 /dev/ttyUSB*
```

然后安装库需要只安装pyserial
```
pip uninstall serial
pip uninstall pyserial

pip install pyserial
```
通信程序：
```
import serial
serial_port = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
serial_port.write("T1\r\n".encode())
str = ""
while True:
    if serial_port.inWaiting() > 0:
        data = serial_port.read().decode()
        if data == '\n':
            print(str)
            str = ""
        else:
            str = str + data
```