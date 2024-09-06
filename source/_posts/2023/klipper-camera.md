---
title: 3D打印机加装摄像头并自动合成延时摄影
tags:
  - 3D打印
cover: /img/klipper.png
categories:
- 折腾记录
date: 2023-08-01 01:08:02
description: 3D打印机加摄像头
---
# 网络摄像头程序
## 安装mjpg-streamer
新版kiauh脚本中已包含crowsnest插件，但是我用的上位机是香橙派zero2，实测安装报错，所以改用经典的mjpg-streamer。这个项目没有实现声音传输，而且已经停止了维护(但是关我拍延时摄影有什么关系)

```
cd ~
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd ~/mjpg-streamer/mjpg-streamer-experimental
sudo make all
sudo make install
```
## 配置
在项目目录内有一个`start.sh`，作为启动脚本，修改其中的启动参数

以我的为例：
```
./mjpg_streamer -i "./input_uvc.so -d /dev/v4l/by-id/usb-SN0002_2K_USB_Camera_46435000_P020300_SN0002-video-index0" -o "./output_http.so -w ./www"
```
其实要改的就是摄像头id

这个命令也可以直接在终端输入，然后打开浏览器查看8080端口网页

## 设置开机启动
在`/etc/rc.local`中，在`exit 0`前写入
```
cd /home/orangepi/mjpg-streamer/
sh start.sh &
cd -
```

# 安装Moonraker-timelapse：

英文安装参考：https://www.obico.io/blog/klipper-timelapse/

## 安装

```
cd ~/ 
git clone https://github.com/mainsail-crew/moonraker-timelapse.git 
cd ~/moonraker-timelapse 
make install
```

在monraker.conf 中最后面加入以下配置(其实不加无所谓)

```
[update_manager timelapse]
type: git_repo
primary_branch: main
path: ~/moonraker-timelapse
origin: https://github.com/mainsail-crew/moonraker-timelapse.git managed_services: klipper moonraker
```

## 配置

配置参考：https://github.com/mainsail-crew/moonraker-timelapse/blob/main/docs/configuration.md

### 在printer.cfg中引用timelapse.cfg文件
打开`printer.cfg`文件在文件开始的地方加入以下代码：

```
[include timelapse.cfg]
```
如果打印机因为找不到这个文件而报错，可以直接在`printer.cfg`的文件夹内创建新文件写入以下内容：
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
max_extrude_only_velocity: 40

[verify_heater extruder]
max_error: 120
hysteresis: 10
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
max_error: 12000
hysteresis: 30
check_gain_time: 300
heating_gain: 1

[fan]
pin: PH6


[mcu]
serial:/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0


[printer]
kinematics: corexy
max_velocity: 180
max_accel: 3000
max_z_velocity: 20
max_z_accel: 300
square_corner_velocity: 10.0


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
z_offset: 1.6
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
#*# 	  0.193750, 0.031250, -0.095000, -0.193750
#*# 	  0.285000, 0.115000, -0.023750, -0.127500
#*# 	  0.388750, 0.185000, 0.052500, -0.026250
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
#*# pid_kp = 10000000
#*# pid_ki = 0
#*# pid_kd = 0
#*#

```

### 设定切片软件

打印机设定->自定义G-code -> 图层更改后 G-Code,框中加入：TIMELAPSE_TAKE_FRAME

### moonraker.conf文件中配置：

打开moonraker.conf文件中添加：

```
[timelapse]
##   Following basic configuration is default to most images and don't need
##   to be changed in most scenarios. Only uncomment and change it if your
##   Image differ from standart installations. In most common scenarios
##   a User only need [timelapse] in there configuration.
#output_path: ~/timelapse/      #文件输出路径 
##   Directory where the generated video will be saved
#frame_path: /tmp/timelapse/   #项目临时存放路径 
##   Directory where the temporary frames are saved
#ffmpeg_binary_path: /usr/bin/ffmpeg
##   Directory where ffmpeg is installed #编译器路径 
########配置选项说明########
#enabled: True #是否启用时间延时摄影
#mode: layermacro #此模式使用宏来触发抓取帧，但需要设置切片器才能在图层更改时添加GCODE
#snapshoturl: http://localhost:8080/?action=snapshot #摄像头调用地址
#gcode_verbose: True # “true”启用或“false”禁用宏的详细程度 
#parkhead: False # “true”启用或“false”禁用在拍摄帧之前移动打印头。 
#parkpos: back_left  #这定义了在拍摄相框之前将打印头停放的位置。可能的配置是[center, front_left, front_right, back_left, back_right, custom]
#如果选择了custom想要自定义打印头驻留的位置可以设置下面的参数
#park_custom_pos_x: 0.0  #自定义打印头驻留的绝对 X 坐标（单位 mm） 
#park_custom_pos_y: 0.0 #自定义打印头驻留的绝对 Y 坐标（单位 mm）
#park_custom_pos_dz: 0.0 # 自定义打印头驻留的相对 Y 坐标（单位 mm） 
#park_travel_speed: 100 #驻留时打印头移动速度（单位毫米/秒
#park_retract_speed: 15  #驻留时缩回速度（单位毫米/秒） 
#park_extrude_speed: 15 # 恢复打印时挤出的速度（单位毫米/秒） 
#park_retract_distance: 1.0 # 回抽来以防止渗出的距离（单位毫米） 
#park_extrude_distance: 1.0 # 恢复打印之前挤出以填充喷嘴的距离（单位 mm） 
#hyperlapse_cycle: 30 #定义在超延时模式下拍摄帧的时间间隔
#autorender: True # “true”启用或“false”禁用打印结束时渲染过程的自动触发。或者，您可以使用最终 gcode 中的“TIMELAPSE_RENDER”或渲染 http 终端节点（可能集成到前端）来触发渲染过程。 
#constant_rate_factor: 23 # 这将配置渲染视频的质量与文件大小。CRF 刻度的范围是 0–51，其中 0 表示无损，23 表示默认值，51 表示质量最差。较低的值通常会导致较高的质量，主观上合理的范围为17-28。将 17 或 18 视为视觉上无损。更多信息：  https://trac.ffmpeg.org/wiki/Encode/H.264 F
#output_framerate: 30 # 定义视频的帧速率。（每秒单位帧数）注意：如果启用了variable_fps，这将被忽略。 
#pixelformat: yuv420p # 定义输出视频的像素格式。一些较旧的h264设备，如手机和其他设备需要“ yuv420p”，这是默认的延时组件。要获取哪些像素格式可用的更多信息，请在系统控制台中运行“ffmpeg -pix_fmts”或参考 ffmpeg 文档：  https://ffmpeg.org/ffmpeg.html 
#time_format_code: %Y%m%d_%H%M # 这定义了应如何命名呈现的视频。它使用 python 日期时间格式。默认值为“%Y%m%d_%H%M”。有关日期时间格式的更多信息，请参阅  此处 https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes 
#extraoutputparams:   定义FFMPEG的额外输出参数 更多信息：   https://ffmpeg.org/ffmpeg.html   注意：在这里指定任何内容可能会禁用其他功能！（ffmpeg 限制） 
#variable_fps: False # “true”启用或“false”禁用输出帧速率的变量计算。这使用拍摄的帧数和“目标长度”，但受“variable_fps_min”和“variable_fps_max”设置的限制。
#targetlength: 10 定义视频的目标长度（单位秒）
#variable_fps_min: 5  variable_fps的最小 fps（每秒帧数）。 
#variable_fps_max: 60 variable_fps的最大 fps（每秒帧数）。
#flip_x: False
#flip_y: False
#duplicatelastframe: 0 #将最后一帧复制到输出视频的末尾。
#previewimage: True #“true”启用或“false”禁用最后一帧来生成预览缩略图
#saveframes: False #“True”启用或“False”禁用将帧打包到 zip 文件以供外部使用或呈现。

```
其实大部分设置都用不到，这是我的配置文件：
```
[timelapse]
parkhead: True
parkpos: custom
park_custom_pos_x: 2.0
park_custom_pos_y: 2.0
park_custom_pos_dz: 0.0
park_travel_speed: 90
park_retract_speed: 25
park_extrude_speed: 25
park_retract_distance: 3.0
```