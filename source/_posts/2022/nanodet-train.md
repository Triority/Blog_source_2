---
title: pytorch环境配置及使用nanodet进行模型训练和识别
date: 2022-11-13 13:01:55
tags:
- python
- 神经网络
- 教程
description: 由于这次需要使用CPU进行识别，同时要求较高帧率，因此使用nanodet而非yolo进行目标识别，同时这也是我第一次尝试模型训练，如有错误欢迎指出
cover: /img/nanodet-plus.jpg
categories: 
- 折腾记录
---
# 环境配置
**这部分内容需要用nvidia显卡，如果只使用CPU识别，那么不需要在识别的电脑上配置，但是训练的电脑建议安装如下内容**
## CUDA安装
### 查看显卡驱动支持的最高CUDA版本
在命令行输入
```
nvidia-smi
```
即可显示支持的最高CUDA版本，例如我的为11.7
![CUDA Version: 11.7](20221114150744.png)
### 安装对应版本CUDA
[官网链接](https://pytorch.org/get-started/locally/ "官网链接")
![官网链接](20221114150417.png)
由于我不打算使用conda，因此选择pip的安装命令
选好之后复制官网下方提供的命令安装
我选择安装到python路径下，因此命令为：
```
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```
其中，务必注意torch和torchvision版本对应，对应关系在这里：[链接](https://github.com/pytorch/vision#installation "链接")
![版本对应关系](20221114151335.png)
### 检查版本是否正确
在python中输入如下命令
```
import torch
import torchvision

torch.__version__
torchvision.__version__
```
如果都不报错，说明安装成功了，且torch和torchvision的版本也已经是对应的，如下:
![注意如果显示+CPU要卸载已安装库再重新安装](20221114151619.png)
注意如果显示+CPU要卸载已安装库再重新安装
至此环境配置结束

# 使用nanodet提供的模型进行识别
由于我们用于识别的设备没有使用Nvidia的GPU，需要使用CPU进行识别，所以在这里使用nanodet一个使用CPU的裁剪版本
[github链接](https://github.com/guo-pu/NanoDet-PyTorch-CPU "github链接")
下载直接能使用，如果想使用原版nanodet：[github链接](https://github.com/RangiLyu/nanodet "github链接")
使用以下命令识别：
```
# 图片文件
python detect_main.py image --config ./config/nanodet-m.yml --model model/nanodet_m.pth --path  street.png

# 视频文件
python detect_main.py video --config ./config/nanodet-m.yml --model model/nanodet_m.pth --path  test.mp4

# 摄像头
python detect_main.py webcam --config ./config/nanodet-m.yml --model model/nanodet_m.pth --path  0
```

# 模型训练
## 数据集准备
首先使用识别用的摄像头拍摄数据集，一共需要几千张左右，可以使用我的自动标注工具生成数据集，那么需要几张识别目标的照片。
## 数据集标注
使用精灵标注助手进行标注，并导出为voc格式，然后使用如下工具，将voc格式数据集转换为coco格式，即可开始训练。
## 使用自己的电脑训练
首先修改配置文件，位于config/xxx.yml。

# 使用自己的模型识别
## 查看识别结果

## 外部调用识别结果
