---
title: klipper做上位机diy的3D打印机
date: 2022-08-31 22:49:36
tags:
- 3D打印
description: 一切开始于fluidd页面真的帅啊hhhhhhhc
cover: /img/klipper.png
categories: 
- [折腾记录]
- [作品&项目总结]
- [值得一提的文章]
---
## 前言
这里主要讲上位机klipper的配置，硬件使用大鱼的设计，主板mks genl2.1，klipper安装于上位机。
mks的说明书已经详细说明了klipper的搭建配置过程：[MKS GEN_L V2.1 Klipper固件使用说明书](https://blog.csdn.net/gjy_skyblue/article/details/121103193 "MKS GEN_L V2.1 Klipper固件使用说明书")
![MKS GEN_L V2.1](MKSGENLSIZE.png)
## 对mks配置文件的修改
### lcd
我没有使用lcd屏，但是mks提供的配置文件`printer.cfg`对lcd进行了配置，需要删除，这一点说明书没有提及，lcd配置include了其他文件，文件在mks的github仓库可以找到。
### pin
我为打印机加装了LED灯带，但是不希望灯一直打开，需要开关功能。由于我没有lcd屏幕，所以可以使用lcd的引脚控制L298N驱动LED灯带。
klipper使用芯片的引脚名称，与marlin不同，mks的github仓库虽然给出来对应关系但是并不完整，具体引脚编号可以查看主板原理图上mega2560芯片的内容。
原理图：
![SCH](SCH.png)
引脚图：
![PIN](PIN.png)

### 我的配置文件
`printer.cfg`
```
# MKS Gen l V2.1

[stepper_x]
step_pin: PF0
dir_pin: PF1
enable_pin: !PD7
microsteps: 16
rotation_distance: 40   ##rotation_distance = ((360°/1.8°) * microsteps) / 80 # # 旋转距离 = （圆周360°/步距角）*细分/每MM脉冲值
endstop_pin:^!PE5 #X-Min, PE4:X-Max
position_endstop: 0
position_max: 290
homing_speed: 60

[stepper_y]
step_pin: PF6
dir_pin: PF7
enable_pin: !PF2
microsteps: 16
rotation_distance: 40
endstop_pin:^!PJ1  #Y-Min, PJ0:Y-Max
position_endstop: 0
position_max: 190
homing_speed: 60

[stepper_z]
step_pin: PL3
dir_pin: !PL1
enable_pin: !PK0
microsteps: 16
rotation_distance: 8
endstop_pin: probe:z_virtual_endstop  #Z-Min, PD2:Z-Max
position_max: 285
position_min: -3
homing_speed: 20

[extruder]
step_pin: PA4
dir_pin: PA6
enable_pin: !PA2
microsteps: 16
rotation_distance: 7.85
nozzle_diameter: 0.4
filament_diameter: 1.750
heater_pin: PB4
sensor_type: ATC Semitec 104GT-2
sensor_pin: PK5
min_temp: 0
max_temp: 270
#control: pid
#pid_Kp: 21.438
#pid_Ki: 0.888
#pid_Kd: 129.435
max_extrude_only_distance: 50000.0
max_extrude_only_velocity: 20
max_extrude_only_accel: 100
pressure_advance = 0.2

[verify_heater extruder]
max_error: 120
hysteresis: 20
check_gain_time: 20
heating_gain: 1

[led LED]
white_pin: PH4
hardware_pwm: True

#[extruder_stepper extra_stepper]
#step_pin: PC1
#dir_pin: !PC3
#enable_pin: !PC7
#microsteps: 16
#rotation_distance: 8
#endstop_pin: ^!PE4
#position_endstop: 0
#position_max: 250
#position_min: -3


[heater_bed]
heater_pin: PH5
sensor_type: ATC Semitec 104GT-2
sensor_pin: PK6
min_temp: -100
max_temp: 180
#control: pid
#pid_kp = 74.551
#pid_ki = 1.053
#pid_kd = 1319.559

[verify_heater heater_bed]
max_error: 1200
hysteresis: 10
check_gain_time: 60
heating_gain: 1

[fan]
pin: PH6


[mcu]
serial:/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0


[printer]
kinematics: corexy
max_velocity: 180
max_accel: 2000
max_z_velocity: 20
max_z_accel: 300
square_corner_velocity: 20.0


[virtual_sdcard]
path: ~/gcode_files

[pause_resume]

[gcode_macro CANCEL_PRINT]
description: Cancel the actual running print
rename_existing: CANCEL_PRINT_BASE
gcode:
  TURN_OFF_HEATERS
  CANCEL_PRINT_BASE


[display_status]

[bltouch]
sensor_pin: ^PD2
control_pin: PB5
x_offset: -9
y_offset: -51
#z_offset: 1.6
speed: 5.0
samples: 2
samples_result: median
sample_retract_dist: 3.0
samples_tolerance: 0.1
samples_tolerance_retries: 1

[safe_z_home]
home_xy_position: 150,100 # Change coordinates to the center of your print bed
speed: 60
z_hop: 20                 # Move up 10mm
z_hop_speed: 10


[gcode_macro G29]
gcode:
    BED_MESH_CLEAR
    G28
    BED_MESH_CALIBRATE
    BED_MESH_PROFILE SAVE=name
    SAVE_CONFIG
    BED_MESH_PROFILE LOAD=name

[bed_mesh]
speed: 120
horizontal_move_z: 10
mesh_min:60,30
mesh_max:240,130
probe_count: 4,3

[include timelapse.cfg]

#*# <---------------------- SAVE_CONFIG ---------------------->
#*# DO NOT EDIT THIS BLOCK OR BELOW. The contents are auto-generated.
#*#
#*# [bed_mesh default]
#*# version = 1
#*# points =
#*# 	  -0.286250, -0.097500, 0.118750, 0.276250
#*# 	  -0.172500, 0.022500, 0.218750, 0.391250
#*# 	  -0.058750, 0.117500, 0.320000, 0.515000
#*# tension = 0.2
#*# min_x = 60.0
#*# algo = lagrange
#*# y_count = 3
#*# mesh_y_pps = 2
#*# min_y = 30.0
#*# x_count = 4
#*# max_y = 130.0
#*# mesh_x_pps = 2
#*# max_x = 240.0
#*#
#*# [extruder]
#*# control = pid
#*# pid_kp = 18.922
#*# pid_ki = 1.078
#*# pid_kd = 83.021
#*#
#*# [heater_bed]
#*# control = pid
#*# pid_kp = 80.0
#*# pid_ki = 100.0
#*# pid_kd = 1000.0
#*#
#*# [bltouch]
#*# z_offset = 1.800


```

`moonraker.conf`:

```
[server]
host: 0.0.0.0
port: 7125
enable_debug_logging: False
klippy_uds_address: /tmp/klippy_uds

[authorization]
trusted_clients:
    10.0.0.0/8
    127.0.0.0/8
    169.254.0.0/16
    172.16.0.0/12
    192.168.0.0/16
    FE80::/10
    ::1/128
cors_domains:
    http://*.lan
    http://*.local
    https://my.mainsail.xyz
    http://my.mainsail.xyz
    https://app.fluidd.xyz
    http://app.fluidd.xyz

[database]
database_path: /home/orangepi/.moonraker_database

[file_manager]
config_path: /home/orangepi/klipper_config
log_path: /home/orangepi/klipper_logs

[octoprint_compat]

[history]

[update_manager]
channel: dev
refresh_interval: 168

[update_manager fluidd]
type: web
channel: stable
repo: fluidd-core/fluidd
path: ~/fluidd

[timelapse]


[notifier print_start]
url: mailto://triority:key@qq.com/?to=triority@qq.com
title: 打印任务已开始
events: started
body: 模型“'{event_args[1].filename}'”开始打印……

[notifier print_complete]

url: mailto://triority:key@qq.com/?to=triority@qq.com
title: 打印任务已完成
events: complete
body: 模型“'{event_args[1].filename}'”打印完成。

[notifier print_error]
url: mailto://triority:key@qq.com/?to=triority@qq.com
title: 打印任务发生错误
events: error
body: 错误：{event_args[1].message}

```
