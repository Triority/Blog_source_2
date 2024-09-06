---
title: 使用v4l2-ctl获取和设置摄像头参数
tags:
  - linux
cover: /img/微信截图_20230626103717.png
categories:
- 文档&笔记
date: 2023-06-26 10:11:05
---
# 安装
```
sudo apt install v4l-utils
```
# 获取信息
## 查看摄像头设备
```
orangepi@orangepizero2:~$ sudo v4l2-ctl --list-devices
cedrus (platform:cedrus):
        /dev/video0
        /dev/media0

2K USB Camera: 2K USB Camera (usb-5311000.usb-1):
        /dev/video1
        /dev/video2
        /dev/media1
```
## 查看摄像头所有参数
```
orangepi@orangepizero2:~$ sudo v4l2-ctl -d /dev/video1 --all
Driver Info:
        Driver name      : uvcvideo
        Card type        : 2K USB Camera: 2K USB Camera
        Bus info         : usb-5311000.usb-1
        Driver version   : 5.16.17
        Capabilities     : 0x84a00001
                Video Capture
                Metadata Capture
                Streaming
                Extended Pix Format
                Device Capabilities
        Device Caps      : 0x04200001
                Video Capture
                Streaming
                Extended Pix Format
Media Driver Info:
        Driver name      : uvcvideo
        Model            : 2K USB Camera: 2K USB Camera
        Serial           : 46435000_P020300_SN0002
        Bus info         : usb-5311000.usb-1
        Media version    : 5.16.17
        Hardware revision: 0x00003000 (12288)
        Driver version   : 5.16.17
Interface Info:
        ID               : 0x03000002
        Type             : V4L Video
Entity Info:
        ID               : 0x00000001 (1)
        Name             : 2K USB Camera: 2K USB Camera
        Function         : V4L2 I/O
        Flags         : default
        Pad 0x01000007   : 0: Sink
          Link 0x0200000d: from remote pad 0x100000a of entity 'Processing 2': Data, Enabled, Immutable
Priority: 2
Video input : 0 (Camera 1: ok)
Format Video Capture:
        Width/Height      : 640/480
        Pixel Format      : 'MJPG' (Motion-JPEG)
        Field             : None
        Bytes per Line    : 0
        Size Image        : 4194304
        Colorspace        : Default
        Transfer Function : Default (maps to Rec. 709)
        YCbCr/HSV Encoding: Default (maps to ITU-R 601)
        Quantization      : Default (maps to Full Range)
        Flags             :
Crop Capability Video Capture:
        Bounds      : Left 0, Top 0, Width 640, Height 480
        Default     : Left 0, Top 0, Width 640, Height 480
        Pixel Aspect: 1/1
Selection Video Capture: crop_default, Left 0, Top 0, Width 640, Height 480, Flags:
Selection Video Capture: crop_bounds, Left 0, Top 0, Width 640, Height 480, Flags:
Streaming Parameters Video Capture:
        Capabilities     : timeperframe
        Frames per second: 30.000 (30/1)
        Read buffers     : 0

User Controls

                     brightness 0x00980900 (int)    : min=1 max=255 step=1 default=128 value=1
                       contrast 0x00980901 (int)    : min=1 max=255 step=1 default=128 value=128
                     saturation 0x00980902 (int)    : min=1 max=255 step=1 default=128 value=255
                            hue 0x00980903 (int)    : min=0 max=255 step=1 default=128 value=128
        white_balance_automatic 0x0098090c (bool)   : default=0 value=1
```
## 查看摄像头的视频压缩格式和支持的分辨率和帧速率
```
orangepi@orangepizero2:~$ sudo v4l2-ctl -d /dev/video1 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.200s (5.000 fps)
                Size: Discrete 1280x960
                        Interval: Discrete 0.200s (5.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.100s (10.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
        [1]: 'MJPG' (Motion-JPEG, compressed)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
                Size: Discrete 2560x1440
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
                Size: Discrete 1280x960
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.040s (25.000 fps)
        [2]: 'NV12' (Y/CbCr 4:2:0)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.200s (5.000 fps)
                Size: Discrete 1280x960
                        Interval: Discrete 0.100s (10.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.067s (15.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
```
# 摄像头参数调整
## 设置分辨率帧率
```
sudo v4l2-ctl -d /dev/video1 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG
sudo v4l2-ctl -d /dev/video1 --set-parm=30
```
## 摄像头参数调整
```
orangepi@orangepizero2:~$ v4l2-ctl -d /dev/video1 --list-ctrls

User Controls

                     brightness 0x00980900 (int)    : min=1 max=255 step=1 default=128 value=1
                       contrast 0x00980901 (int)    : min=1 max=255 step=1 default=128 value=128
                     saturation 0x00980902 (int)    : min=1 max=255 step=1 default=128 value=255
                            hue 0x00980903 (int)    : min=0 max=255 step=1 default=128 value=128
        white_balance_automatic 0x0098090c (bool)   : default=0 value=1
```
修改某个参数的值：
```
v4l2-ctl --device=/dev/video1 --set-ctrl=brightness=1
```

如果是其他摄像头还可能有其他的参数选项，比如我找了一个其他的
```
brightness 0x00980900 (int)    : min=-64 max=64 step=1 default=-40 value=20
                       contrast 0x00980901 (int)    : min=0 max=100 step=1 default=50 value=100//对比度
                     saturation 0x00980902 (int)    : min=0 max=100 step=1 default=50 value=50//饱和度
                            hue 0x00980903 (int)    : min=-180 max=180 step=1 default=0 value=0//色彩
 white_balance_temperature_auto 0x0098090c (bool)   : default=1 value=1//自动白平衡
                          gamma 0x00980910 (int)    : min=100 max=500 step=1 default=300 value=300//伽马，数字越大，图片的亮度也就越高
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=2 value=2
      white_balance_temperature 0x0098091a (int)    : min=2800 max=6500 step=10 default=4600 value=4600 flags=inactive//白平衡
                      sharpness 0x0098091b (int)    : min=0 max=100 step=1 default=50 value=50//锐度
         backlight_compensation 0x0098091c (int)    : min=0 max=2 step=1 default=0 value=0//背光补偿
         exposure_auto_priority 0x009a0903 (bool)   : default=0 value=0
                     focus_auto 0x009a090c (bool)   : default=1 value=0
```
# 更多功能
比如输出视频流之类可以参考[文档](https://www.mankier.com/1/v4l2-ctl)