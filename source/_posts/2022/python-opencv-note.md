---
title: python-opencv学习笔记
description: 在参加智能车竞赛航天物流组线上赛过程中,采用opencv的方式来做赛道识别,所以有了这篇笔记
cover: /img/opencv.png
date: 2022-01-16 17:23:58
categories: 
- [文档&笔记]
- [值得一提的文章]
tags:
- python
- opencv
- 笔记
---
## 基本方法
#### 读取图片
```python
cv2.imread(path_of_image)
cv2.imread(path_of_image, intflag)
```
path_of_image:图片路径

intflag:
CV_LOAD_IMAGE_COLOR    /   1     ------加载彩色图像,忽略透明度.默认
CV_LOAD_IMAGE_GRAYSCALE   /   0     ------灰度模式

#### 窗口显示
```python
cv2.imshow(windows_name, image)
```
windows_name:窗口名称

image:图像对象，类型是numpy中的ndarray类型

#### 窗口关闭
```python
cv2.destroyWindow(windows_name) #关闭单个名为windows_name的窗口
cv2.destroyAllWindows() #关闭全部窗口
```
如果需要一定条件自动关闭窗口:
```python
cv2.waitKey(time_of_milliseconds)
```
当time_of_milliseconds>0时:过time_of_milliseconds毫秒后关闭窗口

当time_of_milliseconds<=0时:等待键盘敲击后关闭.例如:
```python
#当当敲击 Esc 时关闭窗口
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
#当敲击 A 时，关闭名称为'image'的窗口
if cv2.waitKey(-1) == ord('A'):
    cv2.destroyWindow('image')
```
#### 摄像头使用
```python
cap = cv2.VideoCapture(0)#创建摄像头对象,0表示第一个摄像头
```
循环获取并显示:
```python
while(1):
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    if cv2.waitKey(0) == 27:
        break
```
释放摄像头对象:
```python
cap.release()
```
#### 图片保存
```python
cv2.imwrite(image_filename, image)
```
image_filename:文件名称
image:图像对象，类型是numpy中的ndarray类型

## 获取图像信息
#### 获取图片大小及某一点信息
```python
print(rgb_img.shape)     #输出:(1200, 1600, 3):高度height = 1200， 宽度w=1600且通道数为3
print(rgb_img[0, 0])     #输出:[137 124 38]:像素(0,0)的值是(137,124,38),即R=137,G=124,B=38
print(rgb_img[0, 0, 0])  #输出:137:像素(0,0)的R值是137
 
print(gray_img.shape)    #输出:(1200, 1600)
print(gray_img[0, 0])    #输出:100
```
####  获取一整行
```python
#单看第400行的像素
color = img[400]
```
 以白色为例:    获取一行内白色个数
```python
 white_count = np.sum(color == 255)
```
获取白色像素点索引:
```python
 white_index = np.where(color == 255)
```
 应用举例:  求第一个白色点和最后一个白色点横坐标平均值
 ```python
white_count = np.sum(color == 255)
white_index = np.where(color == 255)
# 防止white_count=0的报错
if white_count == 0:
    white_count = 1
center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
print (center)
```
## 图像绘制
#### 创建空白图像
```python
import cv2
import numpy as np
 
white_img = np.ones((512,512,3), np.uint8)   #(512,512,3)代表(宽度,长度,通道)
white_img = 255*white_img
cv2.imshow('white_img', white_img)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
```
一些共有参数:

img:需要进行绘制的图像对象ndarray
color:颜色，采用BGR即上述说的(B、G、R)
thickness:图形中线的粗细，默认为1，对于圆、椭圆等封闭图像取-1时是填充图形内部
lineType:图形线的类型，默认8-connected线是光滑的，当取cv2.LINE_AA时线呈现锯齿状
#### 直线
```python
cv2.line(image, starting, ending, color, thickness, lineType)
```
#### 长方形
```python
cv2.rectangle(image, top-left, bottom-right, color, thickness, lineType)
```
top-left、bottom-right长方形的左上角像素坐标、右下角像素坐标
#### 圆形
```python
cv2.circle(image, center, radius, color, thickness, lineType)
```
center、radius分别表示圆的圆心像素坐标、圆的半径长度
#### 多边形
```python
cv2.polylines(image, [point-set], flag, color, thickness, lineType)
```
[point-set]： 表示多边形点的集合，如果多边形有m个点，则便是一个m12的数组，表示共m个点 flag： 当flag = True 时，则多边形是封闭的，当flag = False 时，则多边形只是从第一个到最后一个点连线组成的图像，没有封闭..示例:

```python
import cv2
import numpy as np
img = np.ones((512,512,3), np.uint8)
img = 255*img
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
img = cv2.polylines(img,[pts],True,(0, 0, 0), 2)
cv2.imshow('img', img)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
```
#### 文字绘制
```python
cv.putText(img,"OpenCV",(10,500),cv.FONT_HERSHEY_SIMPLEX,4,(255,255,255),2,cv_LINE_AA)
cv2.putText(图片img,“文本内容”,(左下角坐标),字体,字体大小,(颜色)，线条粗细，线条类型) 
```

## 图片处理
#### 图像色彩空间变换
```python
cv2.cvtColor(input_image, flag)
```
input_image:要变换色彩的图像ndarray对象
flag:图像色彩空间变换的类型,共有274种空间转换类型,最常用的: 
         cv2.COLOR_BGR2GRAY:将图像从BGR空间转化成灰度图
        cv2.COLOR_BGR2HSV:将图像从BGR空间转化成HSV空间

#### 缩放
```python
#缩放为200*200图像
img1=cv2.resize(img,(200,200))
#缩放至0.5倍
img2=cv2.resize(img,(0,0),fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST)
```
#### 裁剪
```python
#裁剪出竖直方向20-150，水平方向-180到-50这一部分的图像
#原点的为左上角，向右为x轴,向下为y轴
patch_img=img[20:150,-180:-50]
#上一句中负值代表从x轴右侧向左侧选取
```
####  二值化
##### 有阈值的二值化处理

```python
cv2.threshold(src, thresh, maxval, type)
#src：原图片
#thresh：阈值(分割值)
#maxval：最大值
#划分算法:cv2.THRESH_BINARY等
####  大津算法(自动计算阈值)
```

```python
 retval, dst = cv2.threshold(gray, 0, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
```
##### 局部阈值二值化

```python
cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)
#src：进行二值化的图像
#maxValue：将要设置的灰度值
#adaptiveMethod：自适应阈值算法。可选ADAPTIVE_THRESH_MEAN_C 或 ADAPTIVE_THRESH_GAUSSIAN_C
#thresholdType：opencv提供的二值化方法，只能THRESH_BINARY或者THRESH_BINARY_INV
#blockSize：要分成的区域大小，上面的N值，取奇数
#C：常数，每个区域计算出的阈值的基础上在减去这个常数作为这个区域的最终阈值，可以为负数
#dst：输出图像，可忽略
#例子:
img2=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10, dst=None)
```
#### 滤波
```python
#中值滤波
#其中5表示在中心点5*5范围内计算,可改为大于1的奇数
result = cv2.medianBlur(image,5)
#高斯滤波
cv2.GaussianBlur(img,(5,5),1.5)
#均值滤波
cv2.blur(img,(5,5))
# 双边滤波
cv2.bilateralFilter(img,9,75,75)
```

#### 膨胀与腐蚀
```python
#腐蚀
cv2.erode(img,kernel,iterations)
#膨胀
cv2.dilate(img,kernel,iterations)
 
#kernel:内核,如以下两种:
#OpenCV定义的结构矩形元素
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
#NumPy定义的结构元素
NpKernel = np.uint8(np.ones((3,3)))
 
#iterations:进行次数,默认为1次,可以忽略
```
先腐蚀后膨胀，用于移除由图像噪音形成的斑点;（开运算）
先膨胀后腐蚀，用来连接被误分为许多小块的对象.（闭运算）
#### 开运算：用来去除噪声
```python
opening = cv.morphologyEx(noi_src, cv.MORPH_OPEN, kernel)
```
#### 闭运算：用来填充前景物体中的小洞，或前景物体上的小黑点
```python
closing = cv.morphologyEx(noi_src, cv.MORPH_CLOSE, kernel)
```
####  梯度：膨胀与腐蚀的差别，前景物体的轮廓
```python
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
```
#### 图片相减（差异对比）
```python
cv2.absdiff(img1,img2)
```
通过cv2.absdiff(膨胀图像，腐蚀图像)可以获取图像边缘

#### 取反色
```python
cv2.bitwise_not(img)
```
#### 颜色范围选取
```python
lower = np.array([130, 62, 72])
upper = np.array([170, 255, 148])
img = cv2.inRange(frame_hsv, lower, upper)
```
其中lower,upper为HSV空间数组，其中数组中：
        H是色彩
        S是深浅， S = 0时，只有灰度
        V是明暗，表示色彩的明亮程度
        低于或高于数组范围内都将变为0，只有其中间变为255

#### 边缘提取:返回二值图像
```python
img2 = cv.Canny(img,s1,s2)
```
img为输入的灰度图像
s1,s2为低阈值,高阈值.

#### 轮廓检测
```python
cv2.findContours(image, mode, method)
```
image:寻找轮廓的二值图像
mode:轮廓的检索模式
method:轮廓的近似办法
检索模式:
cv2.RETR_EXTERNAL    只检测外轮廓
cv2.RETR_LIST    提取所有轮廓，并放置在list中，检测的轮廓不建立等级关
cv2.RETR_CCOMP    建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
cv2.RETR_TREE    检测所有轮廓，建立完整的层次结构，建立网状轮廓结构 
近似方法:
cv2.CHAIN_APPROX_NONE    获取每个轮廓的每个像素，相邻的两个点的像素位置差不超过1
cv2.CHAIN_APPROX_SIMPLE    压缩水平方向，垂直方向，对角线方向的元素，值保留该方向的重点坐标，如果一个矩形轮廓只需4个点来保存轮廓信息 
cv2.CHAIN_APPROX_TC89_L1    使用Teh-Chini chain近似算法
cv2.CHAIN_APPROX_TC89_KCOS    使用Teh-Chini chain近似算法

注:        如:
```python
returns = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(returns))
```
在cv2中将返回2个值,cv3中将返回3个值
cv2:轮廓本身contours，每条轮廓对应的属性hierarchy
cv3:所处理的图像img, 要找的轮廓的点集countours, 各层轮廓的索引hierarchy

#### 绘制轮廓
```python
cv2.drawContours(image, contours, contourIdx, color)
```
image:需要绘制轮廓的目标图像，会改变原图
contours:轮廓点，上述函数cv2.findContours()的第一个返回值
contourIdx:轮廓的索引，表示绘制第几个轮廓，-1表示绘制所有的轮廓
color:绘制轮廓的颜色
#### 获取外接矩形边框
```python
x,y,w,h = cv2.boundingRect(img)
```
img:一个二值图像
x,y:矩形左上角坐标
w,h:矩形宽高
#### 获取最小旋转外接矩形边框
```python
cv2.minAreaRect(Points)
```
rect[0]返回矩形的中心点，（x,y），y行x列的像素点
	cv2.boxPoints(rect)可以返回四个点的值,返回形式[ [x0,y0], [x1,y1], [x2,y2], [x3,y3] ]
	box = np.int0(box)取得整数
rect[1]返回矩形的长和宽
rect[2]返回矩形的旋转角度

举例:

```python
import cv2 as cv
import numpy as np
img = cv.imread("test.jpg",0)
_,contours,_ = cv.findContours(img,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
rect = cv.minAreaRect(cnt)    #这里得到的是旋转矩形
box = cv.boxPoints(rect)    #得到端点
box = np.int0(box)    #向下取整
```