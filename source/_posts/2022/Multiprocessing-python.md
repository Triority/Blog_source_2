---
title: python使用Multiprocessing库进行多进程执行
date: 2022-07-31 01:56:47
tags:
- python
- 笔记
description: 在使用python进行自动标注过程中，一直使用一个进程，因此运行速度较慢，标注几万张图片需要耗费几个小时，于是想利用多CPU运行自动标注程序...
cover: /img/Multiprocessing.png
categories: 
- 文档&笔记
---
## 前言
在使用python进行自动标注过程中，一直使用一个进程，因此运行速度较慢，标注几万张图片需要耗费几个小时，于是想利用多CPU运行自动标注程序。
单进程自动标注程序可在[以前文章](http://triority.cn/2022/06/21/auto-marking/ "以前文章")找到。
## 多线程
首先想到多线程执行，每个文件夹分一个线程，但是实际运行发现速度并没有提升，仍然使用单个核心运行。查找资料得知：
```
一般来说，编程语言要进行并发编程，多线程会比多进程优先考虑，因为多线程比多进程更省资源。但是由于python底层的GIL的存在，导致了多线程编程时，实际上每个时刻只有一个线程在运行，也即只有一个核被利用起来，并没有起到并行的效果(此说法针对的是cpu密集型的代码，如果是I/O密集型的，多线程还是会有效果的)。于是为了真正利用起来多核，python中需要使用多进程编程。
```
于是。。。
## 多进程库multiprocessing
#### 基本操作流程
在主进程中实例化一个进程池pool对象---->往进程池中放入多个进程---->是否阻塞主进程---->结束
注意，以下内容必须写在程序入口内：
```python
if __name__ == "__main__":
```
#### 实例化进程池pool对象
```python
pool = multiprocessing.Pool(4)
```
其中4指最多使用四个核心，如果加入进程更多，将会是后面的阻塞。
#### 放入多个进程
```python
pool.apply_async(func, (i))
```
`func`是自定义的函数，后面括号为传入参数。
#### 阻塞主进程并执行
在结束之前，需要先关闭进程池，此时不能再加入新的进程。close方法必须在join方法调用前调用：
```python
pool.close()
```
然后阻塞主进程：
```python
pool.join()
```
其他进程结束后结束阻塞。

## 多进程自动标注代码
```python
import cv2
import numpy as np
import random
from funcs import *
import os
import multiprocessing

times = 1
photos = os.listdir(r'photo')
backs = os.listdir(r'back')


def data_maker(img, back, img_copy):
    # 亮度
    img = random_brightness(img)
    back = random_brightness(back)
    # 模糊
    img = random_blur(img)
    # 缩放
    r = random.randint(5, 20) / 10
    img = cv2.resize(img, (0, 0), fx=r, fy=r, interpolation=cv2.INTER_NEAREST)
    img_copy = cv2.resize(img_copy, (0, 0), fx=r, fy=r, interpolation=cv2.INTER_NEAREST)
    # 仿射变换
    img, points = random_horizontally_affine(img)
    xc, yc, wc, hc = points_affine(img_copy, points)
    # 叠加
    back, x, y = overlay(img, back)
    xmin, ymin = (x + xc, y + yc)
    xmax, ymax = (x + xc + wc, y + yc + hc)
    return back, xmin, ymin, xmax, ymax


def kind(datas, backs, times, i):
    m = 0
    n = 0
    for j in datas:
        for k in backs:
            for l in range(0, times):
                m += 1
                n += 1
                img = cv2.imread('photo\\' + i + '\\' + j)
                back = cv2.imread('back\\' + k)
                rbn = backs[random.randint(0, len(backs) - 1)]
                back[0:539, 960:1919] = cv2.imread('back\\' + rbn)[0:539, 960:1919]
                rbn = backs[random.randint(0, len(backs) - 1)]
                back[540:1079, 0:969] = cv2.imread('back\\' + rbn)[540:1079, 0:969]
                rbn = backs[random.randint(0, len(backs) - 1)]
                back[540:1079, 960:1919] = cv2.imread('back\\' + rbn)[540:1079, 960:1919]
                img_copy = cv2.imread('photo_copy\\' + i + '\\' + j)
                save, xmin, ymin, xmax, ymax = data_maker(img, back, img_copy)
                cv2.imwrite("F:\\out\\photo_output\\" + i + '\\' + str(m) + '.jpg', save)
                cv2.rectangle(save, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.imwrite("F:\\out\\photo_marked\\" + i + '\\' + str(m) + '.jpg', save)
                # print((m, xmin, ymin, xmax, ymax))
                txt = xml_save(str(m) + '.jpg', str(xmin), str(ymin), str(xmax), str(ymax))
                path = 'F:\\out\\outputs\\' + i + '\\' + str(m) + '.xml'
                fw = open(path, 'w')
                fw.write(txt)
                fw.close()
                xx = xmax - xmin
                yy = ymax - ymin
                if not 0.2 < xx / yy < 2:
                    m -= 1
                print(i + '进度：' + str(n) + '/' + str(len(datas) * len(backs) * times))


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=16)
    for i in photos:
        datas = os.listdir('photo\\' + i)
        pool.apply_async(kind, (datas, backs, times, i))
    pool.close()
    pool.join()
    print("Sub-process(es) done.")

```