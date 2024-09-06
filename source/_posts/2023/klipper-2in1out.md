---
title: 3D打印机改装两进一出
tags:
  - 3D打印
cover: /img/klipper.png
categories:
- 折腾记录
date: 2023-07-10 00:59:09
description: 3D打印机改装两进一出
---
# 两进一出加热头
改了两进一出双色挤出头，配置文件改成这样:

```
# MKS Gen l V2.1
[include timelapse.cfg]

[stepper_x]
step_pin: PF0
dir_pin: PF1
enable_pin: !PD7
microsteps: 16
rotation_distance: 40   ##rotation_distance = ((360°/1.8°) * microsteps) / 80 # # 旋转距离 = （圆周360°/步距角）*细分/每MM脉冲值
endstop_pin:^!PE5 #X-Min, PE4:X-Max
position_endstop: 0
position_max: 295
homing_speed: 30

[stepper_y]
step_pin: PF6
dir_pin: PF7
enable_pin: !PF2
microsteps: 16
rotation_distance: 40
endstop_pin:^!PJ1  #Y-Min, PJ0:Y-Max
position_endstop: 0
position_max: 205
homing_speed: 30

[stepper_z]
step_pin: PL3
dir_pin: !PL1
enable_pin: !PK0
microsteps: 16
rotation_distance: 8
endstop_pin: probe:z_virtual_endstop  #Z-Min, PD2:Z-Max
position_max: 260
position_min: -3

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

[verify_heater extruder]
max_error: 1200
hysteresis: 20
check_gain_time: 20
heating_gain: 1

[extruder_stepper belted_extruder]
extruder: extruder
step_pin: PC1
dir_pin: !PC3
enable_pin: !PC7
microsteps: 16
rotation_distance: 7.85

[gcode_macro T0]
gcode:
    # Deactivate stepper in my_extruder_stepper
    SYNC_STEPPER_TO_EXTRUDER STEPPER=belted_extruder EXTRUDER=
    # Activate stepper in extruder
    SYNC_STEPPER_TO_EXTRUDER STEPPER=extruder EXTRUDER=extruder

[gcode_macro T1]
gcode:
    # Deactivate stepper in extruder
    SYNC_STEPPER_TO_EXTRUDER STEPPER=extruder EXTRUDER=
    # Activate stepper in my_extruder_stepper
    SYNC_STEPPER_TO_EXTRUDER STEPPER=belted_extruder EXTRUDER=extruder

[gcode_macro ACTIVATE_EXTRUDER]
description: Replaces built-in macro for a X-in, 1-out extruder configuration SuperSlicer fix
rename_existing: ACTIVATE_EXTRUDER_BASE
gcode:
    {% if 'EXTRUDER' in params %}
      {% set ext = params.EXTRUDER|default(EXTRUDER) %}
      {% if ext == "extruder"%}
        {action_respond_info("Switching to extruder0.")}
        T0
      {% elif ext == "extruder1" %}
        {action_respond_info("Switching to extruder1.")}
        T1
      {% else %}
        {action_respond_info("EXTRUDER value being passed.")}
        ACTIVATE_EXTRUDER_BASE EXTRUDER={ext}
      {% endif %}
    {% endif %}

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
max_velocity: 3000
max_accel: 3000
max_z_velocity: 20
max_z_accel: 300
square_corner_velocity: 300.0

[output_pin Camera_control]
pin: PC4

[fan_generic LED]
pin: PL0
shutdown_speed: 1.0

[fan_generic Camera_X]
pin: PG5
max_power: 0.125
cycle_time: 0.02

[fan_generic Camera_Y]
pin: PE3
max_power: 0.125
cycle_time: 0.02

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
x_offset: 36
y_offset: 0
z_offset: 3.150
speed: 5.0
samples: 2
samples_result: median
sample_retract_dist: 3.0
samples_tolerance: 0.1
samples_tolerance_retries: 1

[safe_z_home]
home_xy_position: 150,100 # Change coordinates to the center of your print bed
speed: 50
z_hop: 10                 # Move up 10mm
z_hop_speed: 5


[gcode_macro G29]
gcode:
    BED_MESH_CLEAR
    G28
    BED_MESH_CALIBRATE
    BED_MESH_PROFILE SAVE=name
    SAVE_CONFIG
    BED_MESH_PROFILE LOAD=name

[bed_mesh]
speed: 100
horizontal_move_z: 5
mesh_min:60,40
mesh_max:260,160
probe_count: 3,3

#*# <---------------------- SAVE_CONFIG ---------------------->
#*# DO NOT EDIT THIS BLOCK OR BELOW. The contents are auto-generated.
#*#
#*# [bed_mesh default]
#*# version = 1
#*# points =
#*# 	  -0.045000, -0.012500, -0.070000
#*# 	  0.182500, 0.061250, 0.008750
#*# 	  0.175000, 0.012500, 0.015000
#*# tension = 0.2
#*# min_x = 60.0
#*# algo = lagrange
#*# y_count = 3
#*# mesh_y_pps = 2
#*# min_y = 40.0
#*# x_count = 3
#*# max_y = 160.0
#*# mesh_x_pps = 2
#*# max_x = 260.0
#*#
#*# [extruder]
#*# control = pid
#*# pid_kp = 19.454
#*# pid_ki = 0.675
#*# pid_kd = 140.071
#*#
#*# [heater_bed]
#*# control = pid
#*# pid_kp = 1000
#*# pid_ki = 0.0
#*# pid_kd = 0.0

```

其中挤出头部分的机械机构是自己设计的，感觉十分逆天：
![](Cache_-79fa417b78e11c7e.jpg)

把touch放在后面，前面就看不见不对称了hhh

可惜原来的模型文件找不到了，只有截图了

# 自制多色
前面说的那种挤出头不是很好用，经常堵头而且流量很低。所以想自己设计一个两进一出，继续使用原来的V6挤出头，所以现在已经换回V6挤出头了，换色想用在挤出头进料处加装打印的Y形气动接头连接件实现。