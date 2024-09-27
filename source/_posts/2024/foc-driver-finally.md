---
title: FOC电机驱动器项目总结
tags:
  - PCB设计
  - 电力电子
  - esp32
  - 单片机
cover: /img/3ff5fd67c30ac14c014e009861d6d0e.jpg
categories:
  - 值得一提的文章
  - 折腾记录
  - 作品&项目总结
date: 2024-07-02 14:05:33
description: simplefoc驱动all in one
---
# 小功率主控驱动集成设计
PCB专为4010/4008无刷云台电机设计，集成了esp32主控，drv8313驱动，as5600磁编码器，can总线通讯控制，ina240在线三相电流采样放大(这部分独立出来可选插装，因为这个芯片太贵了而且不是每个板子都用)

## 硬件设计
### 原理图[下载](ProDoc_P1_2024-07-02.epro)
{% pdf SCH_Schematic1_1_2024-07-02.pdf %}

### PCB[下载](ProDoc_PCB5_2024-07-02.epro)
![](微信截图_20240702154730.png)
### 3D及实物
#### 底板
| ![](微信截图_20240702155112.png) |  |
| :---: | :---: |
| 3D | 照片 |
| <img width=2000/> | <img width=2000/> |

#### 电流检测插件

| 原理图 | ![](微信截图_20240702160102.png) | ![](微信截图_20240702160152.png) |
| :---: | :---: | :---: |
| PCB | ![](微信截图_20240702155918.png) | ![](微信截图_20240702155932.png) |
| 说明 | [SOIC8封装的INA240A2DR](ProDoc_PCB2_2024-07-02.epro) | [TSSOP8封装的INA240A2PWR](ProDoc_PCB2_1_2024-07-02.epro) |
|  | <img width=2000/> | <img width=2000/> |

## 软件

{% note info modern %}
这部分使用simplefoc，对硬件进行简单测试用。实际项目中使用的代码可以在项目的文章中找到
{% endnote %}

### 位置闭环控制

```c
#include <SimpleFOC.h>

MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

// BLDC motor & driver instance
BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(25, 26, 27, 14);

// angle set point variable
float target_angle = 0;
// instantiate the commander
Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&target_angle, cmd); }

void setup() {

  // initialise magnetic sensor hardware
  sensor.init();
  // link the motor to the sensor
  motor.linkSensor(&sensor);

  // driver config
  // power supply voltage [V]
  driver.voltage_power_supply = 12;
  driver.init();
  // link the motor and the driver
  motor.linkDriver(&driver);

  // choose FOC modulation (optional)
  motor.foc_modulation = FOCModulationType::SpaceVectorPWM;

  // set motion control loop to be used
  motor.controller = MotionControlType::angle;

  // contoller configuration
  // default parameters in defaults.h

  // velocity PI controller parameters
  motor.PID_velocity.P = 0.2f;
  motor.PID_velocity.I = 20;
  motor.PID_velocity.D = 0;
  // maximal voltage to be set to the motor
  motor.voltage_limit = 6;

  // velocity low pass filtering time constant
  // the lower the less filtered
  motor.LPF_velocity.Tf = 0.01f;

  // angle P controller
  motor.P_angle.P = 20;
  // maximal velocity of the position control
  motor.velocity_limit = 20;

  // use monitoring with serial
  Serial.begin(115200);
  // comment out if not needed
  motor.useMonitoring(Serial);


  // initialize motor
  motor.init();
  // align sensor and start FOC
  motor.initFOC();

  // add target command T
  command.add('T', doTarget, "target angle");

  Serial.println(F("Motor ready."));
  Serial.println(F("Set the target angle using serial terminal:"));
  _delay(1000);
}


void loop() {

  // main FOC algorithm function
  // the faster you run this function the better
  // Arduino UNO loop  ~1kHz
  // Bluepill loop ~10kHz
  motor.loopFOC();

  // Motion control function
  // velocity, position or voltage (defined in motor.controller)
  // this function can be run at much lower frequency than loopFOC() function
  // You can also use motor.move() and set the motor.target in the code
  motor.move(target_angle);


  // function intended to be used with serial plotter to monitor motor variables
  // significantly slowing the execution down!!!!
  // motor.monitor();

  // user communication
  command.run();
}
```

### 速度闭环控制

```c
#include <SimpleFOC.h>

MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

// BLDC motor & driver instance
BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(25, 26, 27, 14);

// velocity set point variable
float target_velocity = 0;
// instantiate the commander
Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&target_velocity, cmd); }

void setup() {

  // initialise magnetic sensor hardware
  sensor.init();
  // link the motor to the sensor
  motor.linkSensor(&sensor);

  // driver config
  // power supply voltage [V]
  driver.voltage_power_supply = 12;
  driver.init();
  // link the motor and the driver
  motor.linkDriver(&driver);

  // set motion control loop to be used
  motor.controller = MotionControlType::velocity;

  // contoller configuration
  // default parameters in defaults.h

  // velocity PI controller parameters
  motor.PID_velocity.P = 0.2f;
  motor.PID_velocity.I = 20;
  motor.PID_velocity.D = 0;
  // default voltage_power_supply
  motor.voltage_limit = 6;
  // jerk control using voltage voltage ramp
  // default value is 300 volts per sec  ~ 0.3V per millisecond
  motor.PID_velocity.output_ramp = 1000;

  // velocity low pass filtering
  // default 5ms - try different values to see what is the best.
  // the lower the less filtered
  motor.LPF_velocity.Tf = 0.01f;

  // use monitoring with serial
  Serial.begin(115200);
  // comment out if not needed
  motor.useMonitoring(Serial);

  // initialize motor
  motor.init();
  // align sensor and start FOC
  motor.initFOC();

  // add target command T
  command.add('T', doTarget, "target velocity");

  Serial.println(F("Motor ready."));
  Serial.println(F("Set the target velocity using serial terminal:"));
  _delay(1000);
}

void loop() {
  // main FOC algorithm function
  // the faster you run this function the better
  // Arduino UNO loop  ~1kHz
  // Bluepill loop ~10kHz
  motor.loopFOC();

  // Motion control function
  // velocity, position or voltage (defined in motor.controller)
  // this function can be run at much lower frequency than loopFOC() function
  // You can also use motor.move() and set the motor.target in the code
  motor.move(target_velocity);

  // function intended to be used with serial plotter to monitor motor variables
  // significantly slowing the execution down!!!!
  // motor.monitor();

  // user communication
  command.run();
}

```

### 力矩(foc电流)闭环控制

![](https://docs.simplefoc.com/extras/Images/foc_current_mode.png)

```c
#include <SimpleFOC.h>

// BLDC motor & driver instance
BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(25, 26, 27, 14);

MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

// current sensor
InlineCurrentSense current_sense = InlineCurrentSense(0.01f, 50.0f, 34, 35, 36);

// instantiate the commander.2

Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&motor.target, cmd); }

void setup() { 
  // initialise magnetic sensor hardware
  sensor.init();
  // link the motor to the sensora
  motor.linkSensor(&sensor);

  // driver config
  // power supply voltage [V]
  driver.voltage_power_supply = 18;
  driver.init();
  // link driver
  motor.linkDriver(&driver);
  // link the driver to the current sense
  current_sense.linkDriver(&driver);

  // current sense init hardware
  current_sense.init();
  // link the current sense to the motor
  motor.linkCurrentSense(&current_sense);

  // set torque mode:
  motor.torque_controller = TorqueControlType::foc_current; 
  // set motion control loop to be used
  motor.controller = MotionControlType::torque;

  // foc current control parameters (Arduino UNO/Mega)
  motor.PID_current_q.P = 5;
  motor.PID_current_q.I= 300;
  motor.PID_current_d.P= 5;
  motor.PID_current_d.I = 300;
  motor.LPF_current_q.Tf = 0.01; 
  motor.LPF_current_d.Tf = 0.01; 

  // use monitoring with serial 
  Serial.begin(115200);
  // comment out if not needed
  motor.useMonitoring(Serial);

  // initialize motor
  motor.init();
  // align sensor and start FOC
  motor.initFOC();

  // add target command T
  command.add('T', doTarget, "target current");

  Serial.println(F("Motor ready."));
  _delay(1000);
}

void loop() {

  // main FOC algorithm function
  motor.loopFOC();

  // Motion control function
  motor.move();

  // user communication
  command.run();
}
```

## 应用
2023年电赛期间，当时虽然还没做力矩闭环，但是已经完成的位置闭环已经足够完成E类控制题了，当时用的网上买来的数字舵机精度不满足要求(激光笔云台3m外指向精度1cm以内),当场用两个4010做了个新云台，精度不知道高了几个数量级

到写这篇总结时候虽然已经过去一年了，但是东西还在，随手拿起来拍张照片吧，电赛那四天三夜也是很难忘的经历了

| ![](21b15661c5ad6a7de24ad9e7f6cc525.jpg) | 当时做的两轴激光笔云台，集成esp32,as5600,drv8313，当时还没做好电流检测，精度的限制已经不在于执行硬件了，变成激光定位算法了。 |
| :---: | :---: |
| <img width=2000/> | <img width=2000/> |


# 大功率驱动设计
这个驱动没有集成主控需要输入三相PWM信号进行控制
## 原理图[下载](SCH_EG2104+NCE6080_2024-07-02.json)
{% pdf Schematic_EG2104+NCE6080_2024-07-02.pdf %}

## PCB[下载](PCB_PCB_EG2104+NCE6080_2_2024-07-02.json)
![](微信截图_20240702152608.png)

## 3D及实物
| ![](微信截图_20240702152849.png) | ![](3d9015afaf27f26da5a2927097fa7ce.jpg) |
|:---:|:---:|
| 3D | 照片 |
| <img width=2000/> | <img width=2000/> |

# 特别感谢

[Simplefoc Project](https://www.simplefoc.com/)
[JLC](https://www.jlc.com/)
2023年电赛电源组学长，QQX
