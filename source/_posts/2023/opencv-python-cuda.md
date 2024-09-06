---
title: opencv-python库使用cuda加速
tags:
  - opencv
  - python
cover: /img/opencv.png
categories:
- 折腾记录
notshow: true
date: 2023-04-16 20:44:17
description: 使用cuda加速opencv
---
# 安装环境
## CUDA Toolkit
[注意与显卡驱动版本相匹配](https://developer.nvidia.com/cuda-toolkit-archive)
## cuDNN
[注意CUDA版本](https://developer.nvidia.com/rdp/cudnn-archive)
将压缩包里面的三个文件夹放入`CUDA Toolkit`安装目录，默认路径
```
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7
```
## 下载预构建的opencv源代码
[预构建的opencv源代码](https://jamesbowley.co.uk/downloads/#OpenCV4.5.0)

`opencv_4_5_0_cuda_11_1_py38.7z`文件解压后，得到两个文件夹，`install`和`lib`

`install`文件夹，依次进入路径`install\x64\vc16\bin`，然后添加将其到系统环境变量中

`lib\python3\cv2.cp38-win_amd64.pyd`文件复制放入自己python环境的`site-packages`中

## 查看已安装的opencv是否支持cuda
```
import cv2
print(cv2.cuda.getCudaEnabledDeviceCount())
```
如果返回值大于0，则说明OpenCV已经安装了CUDA支持
