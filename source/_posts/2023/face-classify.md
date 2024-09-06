---
title: 人脸识别图像分类
date: 2023-01-07 11:15:27
tags:
- python
description: 人脸识别图像分类
cover: /img/syk3.jpg
categories: 
- 折腾记录
---
## 人脸识别
### 人脸识别的基本过程
+ 人脸的 68 个基本特征点位置以及顺序。判断 68 个特征点在图像上面是否存在、是否完整；
+ 人脸 detect，这一步主要就是定位人脸在图像中的位置，利用目标检测算法输出人脸位置矩形框；
+ 人脸 shape predictor，这一步就是要找出眼睛眉毛鼻子嘴巴具体的点位；
+ 人脸对齐 alignment，这一步主要是通过投影几何变换出一张标准脸；
+ 人脸识别，这一步就是在对挤的人脸图像上提取 128 维的特征向量，根据特征向量间的距离来进行判断识别。

python 中最常用的人脸识别库是基于 C++ 开发的 `dlib` 库。

`face_recognition` 库是基于 `dlib` 进行了二次封装，号称世界上最简洁的人脸识别库

### 库的安装
`dlib`库目前已经编译好的安装版本只支持 python 3.6 的版本，由于我安装的环境是 python 3.8，因此这里提供一个网络上找到的[编译好的whl文件](dlib-19.19.0-cp38-cp38-win_amd64.whl)

`face_recognition` 库：
> pip install -i https://pypi.douban.com/simple face_recognition

### 方法
#### 定位人脸位置

```
# -*-coding:GBK -*-
import face_recognition
from PIL import Image
import cv2
 
# 通过 load_image_file 方法加载待识别图片
image = image = cv2.imread('girls.jpg')
 
# 通过 face_locations 得到图像中所有人脸位置
face_locations = face_recognition.face_locations(image)
 
for face_location in face_locations:
    top, right, bottom, left = face_location   # 结报操作，得到每张人脸的四个位置信息
    print("已识别到人脸部位，限速区域为：top{}, right{}, bottom{}, left{}".format(top, right, bottom, left))
    # face_image = image[top:bottom, left:right]
    # pil_image = Image.fromarray(face_image)
    # pil_image.show()
    start = (left, top)
    end = (right, bottom)
 
    # 在图片上绘制矩形框
    cv2.rectangle(image, start, end, (0,0,255), thickness=2)
 
cv2.imshow('window', image)
cv2.waitKey()
```

![face_range](face_range.png)
#### 人脸关键特征点识别
`face_landmarks` 识别人脸关键特征点。返回值是包含面部特征点字典的列表，列表长度就是图像中的人脸数。

面部特征包括以下几个部分：nose_bridge (鼻梁)、right _eyebrow (右眼眉)、left_eyebrow (左眼眉)、right_eye（右眼)、left_eye（左眼)、chin(下巴)、 nose_tip（下鼻部） 、bottom_lip (下嘴唇) 

```
# -*-coding:GBK -*-
import face_recognition
from PIL import Image, ImageDraw
 
image = face_recognition.load_image_file('E:/boys.jpg')
 
face_landmarks_list = face_recognition.face_landmarks(image)
 
pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)   # 生成一张PIL图像
 
for face_landmarks in face_landmarks_list:
    facial_features = [
        'chin',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'left_eye',
        'right_eye',
        'bottom_lip'
    ]
    for facial_feature in facial_features:
        # print("每个人的面部特征显示在以下为位置：{}".format(facial_feature))
        d.line(face_landmarks[facial_feature], width=5)   # 直接调用PIL中的line方法在PIL图像中绘制线条，帮助我们观察特征点
 
pil_image.show()
```

![face_landmarks](face_landmarks.png)

#### 面部信息识别与匹配
`face_encodings` 获取图像文件中所有面部编码信息。

返回值是一个编码列表，参数仍然是要识别的图像对象。如果后续访问时，需要注意加上索引或遍历来进行访问。每张人脸的编码信息是一个 128 维向量。
面部编码信息是进行人像对比的重要参数。
```
# -*-coding:GBK -*-
import face_recognition
 
image = face_recognition.load_image_file('E:/boys.jpg')
 
# 返回值是一个列表
face_encodings = face_recognition.face_encodings(image)
for face_encoding in face_encodings:
    print("信息编码长度为：{}\n编码信息为：{}".format(len(face_encoding), face_encoding))
```

`compare_faces` 由面部编码信息进行面部识别匹配。

主要用于匹配两个面部特征编码，利用这两个特征向量的内积来衡量相似度，根据阈值确认是否是同一个人。
第一个参数就是一个面部编码列表， 第二个参数就是给出单个面部编码， compare_faces 会将第二个参数中的编码信息与第一个参数中的所有编码信息依次匹配，返回值是一个布尔列表，匹配成功则返回 True，匹配失败则返回 False，顺序与第一个参数中脸部编码顺序一致。
参数里有一个 `tolerance = 0.6`，可以根据实际的效果进行调整，一般经验值是 `0.39`。`tolerance` 值越小，匹配越严格。

```
# -*-coding:GBK -*-
import face_recognition
 
# 加载一张合照
image1 = face_recognition.load_image_file('2.jpeg')
# 加载一张单人照
image2 = face_recognition.load_image_file('1.jpg')

known_face_encodings = face_recognition.face_encodings(image1)

compare_face_encodings = face_recognition.face_encodings(image2)[0]

matches = face_recognition.compare_faces(known_face_encodings, compare_face_encodings)
print(matches)
```
## 图像分类
