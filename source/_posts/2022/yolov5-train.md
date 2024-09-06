---
title: yolov5数据集训练
date: 2022-12-10 17:52:20
tags:
- python
- 神经网络
description: yolov5数据集训练
cover: /img/yolov5.png
categories: 
- 折腾记录
---
## 下载yolov5
```
git clone https://github.com/ultralytics/yolov5
```
## 训练
### 数据集
使用yolo格式数据集：
datasets/
└images/
.  └10001.jpg
.  └10002.jpg
.  └......
└labels/
.  └10001.txt
.  └10001.txt
.  └......
└classes.names
`xxx.txt`:`0  0.160938  0.541667  0.120312  0.386111`
分别指：`类别序号`、归一化后的`中心点x`坐标，归一化后的`中心点y`坐标，归一化后的`目标框宽度w`，归一化后的`目标框高度h`
`classes.names`:多行文本，分别为所有的类别名称
### 训练参数
由于我们不使用预训练模型，因此训练需要把`train.py`中的`weights`默认参数设为空，即改为`parser.add_argument('--weights', type=str, default='', help='initial weights path')`

还需要修改 `xxx.yaml`和` yolov5s.yaml`：

 `xxx.yaml`是数据集的配置文件，位于data文件夹内，需要修改内容如下：
```
path: data/datasets/YOLO-QR-datasets  # dataset root dir
train: Dataset2/images  # train images (relative to 'path')
val: Dataset1/images  # val images (relative to 'path')
test:  # test images (optional)
names:
  0: QR
```
`path`为数据集目录，`train`为其中的训练集图片目录，`val`验证集图片目录，`test`测试集图片目录可选
训练启动时会自动将路径中的`images`替换为`labels`作为标注文件的路径。
如果只有一个要识别的类别，则`names`只需一项`0`，即数据集的类别序号，后面是其名称。

` yolov5s.yaml`是模型的配置文件，其他可选的还有` yolov5m.yaml`，` yolov5l.yaml`等，按照需求选择模型大小后，需要修改的主要为`nc: 80  # number of classes`，但是后来发现即使不改启动训练之后也会用读取到的正确类别数量替换这一数值。

使用命令：`python train.py --data xxx.yaml --cfg yolov5s.yaml --img 640`开始训练。
### 可视化及模型分析评估
在同目录终端中使用`tensorboard --logdir runs\train`打开tensorboard可视化工具，在`http://localhost:6006/`中查看数据
训练程序运行中输出的数据：`box_loss` 定位损失，预测框与标定框之间的误差。  `obj_loss` 置信度损失，计算网络的置信度。  `cls_loss` 分类损失，计算锚框与对应的标定分类是否正确。
### 结果输出
训练得到的最佳模型保存于`run/train/expx/weights/best.pt`
