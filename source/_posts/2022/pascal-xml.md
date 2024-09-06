---
title: 数据集pascal-xml格式转xml格式
description: 把pascal格式的数据集输出改为xml格式
cover: /img/pascal-xml.png
date: 2022-06-28 21:45:44
tags:
- python
- 神经网络
categories: 
- 折腾记录
---

## 前言
在之前的数据集标注中，导出的格式是pascal，完成以后我就删掉了记录，后来由于一些错误，需要对原来的数据集进行修改，但是pascal格式不支持导入，因此有了转换成xml格式的需求。

## XML
首先观察xml格式的输出文件，拿出一个作为模板，只需修改其中的path以及x,y的max,min即可。
下一步就是读取pascal格式的xml文件。
这里使用了`from xml.etree import ElementTree as ET`的方法
```python
#读取xml文件
tree = ET.parse(path)
#获取根节点(root)
root = tree.getroot()
#在根节点(root)寻找object节点
object = root.find('object')
#在object节点中读取xmin的值
xmin = bndbox.find('xmin').text
```

## 代码
这里的代码还加入了寻找漏标项目的功能，输出其文件名和位置
此外此方法还可以自动去除多标的情况
另外在列表中查询指定值的索引的代码在这次编程中才学会
`filenames.index(i)`返回filenames列表中i的出现位置索引
下面是全部代码：
默认是从`outputs(pet)`读取pascal格式，然后输出xml格式到`outputs`文件夹
```python
import os
import time
import keyboard
import pyautogui
from xml.etree import ElementTree as ET
er=[]
th=[]
filenames = os.listdir(r'outputs(pet)')
for i in filenames:
    try:
        path = 'outputs(pet)\\'+i
        tree = ET.parse(path)
        root = tree.getroot()
        object = root.find('object')
        bndbox = object.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        print(xmin, ymin, xmax, ymax)
        path = i[0:-4]
        str = """<?xml version="1.0" ?>
<doc>
	<path>F:\\air2\\pet\\"""+path+""".jpg</path>
	<outputs>
		<object>
			<item>
				<name>pet</name>
				<bndbox>
					<xmin>"""+xmin+"""</xmin>
					<ymin>"""+ymin+"""</ymin>
					<xmax>"""+xmax+"""</xmax>
					<ymax>"""+ymax+"""</ymax>
				</bndbox>
			</item>
		</object>
	</outputs>
	<time_labeled>1656409300728</time_labeled>
	<labeled>true</labeled>
	<size>
		<width>1920</width>
		<height>1080</height>
		<depth>3</depth>
	</size>
</doc>
"""
        path = 'outputs\\'+i
        fw = open(path, 'w')
        fw.write(str)
        fw.close()
    except AttributeError:
        er.append(i)
        th.append(filenames.index(i)+1)
print(er)
print(th)

```
