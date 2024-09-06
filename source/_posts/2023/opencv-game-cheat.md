---
title: 使用opencv在小游戏作弊
tags:
  - opencv
  - python
cover: /img/微信截图_20230607003814.png
categories:
- [整活&游戏]
- [折腾记录]
notshow: false
date: 2022-04-01 01:23:59
description: 考验眼力的时候到了
---
用于这个地址的小游戏

https://www.webhek.com/post/color-test.html

实测每分钟可达1000个以上
实际效果取决于您的CPU
可能需要根据屏幕分辨率来修改坐标点

main.py
```
import time
import win32gui, win32ui, win32con, win32api
import pyautogui
import statistics
from ctypes import windll
import numpy as np
#两次操作间隔时间
tx=0.0005
#六个计时项目
t1=[]
t2=[]
t3=[]
t4=[]
t5=[]
t6=[]
time.sleep(2)
#找到数组中不一样的数组函数
def compare(a):
    if all(a[0] == a[1]):
        x = 0
        for i in range(0, len(a)+1):
            if all(a[0] == a[i]):
                x = x+1
            else:
                return x
    elif all(a[0] == a[2]):
        return 1
    elif all(a[1] == a[2]):
        return 0
    else:
        return -1

#识别函数,m=x坐标,n=y坐标,p=间距,q=个数
t = time.time()
def picture(m,n,p,q):
    global t
    t6.append(time.time() - t)
    t = time.time()
    jpg = pyautogui.screenshot(region=[0, 0, 1920, 1080])
    t1.append(time.time()-t)
    t = time.time()
    jpg = np.asarray(jpg)
    t2.append(time.time() - t)
    t = time.time()
    a = []
    for i in range(0, q):
        for j in range(0, q):
            a.append(jpg[n+i*p, m+j*p])
            print([n+i*p, m+j*p])
    t3.append(time.time() - t)
    t = time.time()
    y = compare(a)
    t4.append(time.time() - t)
    t = time.time()
    windll.user32.SetCursorPos(m+y%q*p, n+y//q*p)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, m+y%q*p, n+y//q*p)
    time.sleep(0.0001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, m+y%q*p, n+y//q*p)
    t5.append(time.time() - t)
    t = time.time()
    print([m+y%q*p, n+y//q*p])

#点击开始按键
pyautogui.click(950,850,button='left')
#图片识别
picture(850,350,300,2)
time.sleep(tx)
picture(800,300,200,3)
time.sleep(tx)
picture(760,240,150,4)
time.sleep(tx)
picture(750,220,130,5)
time.sleep(tx)
picture(750,220,130,5)
time.sleep(tx)
picture(740,210,100,6)
time.sleep(tx)
picture(740,210,100,6)
time.sleep(tx)
picture(730,200,90,7)
time.sleep(tx)
picture(730,200,90,7)
time.sleep(tx)
picture(730,200,90,7)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
picture(730,200,80,8)
time.sleep(tx)
try:
    for r in range(0,1000):
        picture(720,190,70,9)
        time.sleep(tx)
except:
    pass
#显示每步平均用时
mean1 = statistics.mean(t1)
mean2 = statistics.mean(t2)
mean3 = statistics.mean(t3)
mean4 = statistics.mean(t4)
mean5 = statistics.mean(t5)
mean6 = statistics.mean(t6)
print('截图'+str(mean1))
print('读取'+str(mean2))
print('取色'+str(mean3))
print('比较'+str(mean4))
print('点击'+str(mean5))
print('间隔'+str(mean6))
```