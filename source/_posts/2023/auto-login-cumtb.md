---
title: 百抗校园网自动登录
tags:
  - python
  - web
cover: /img/selenium.webp
categories:
- 折腾记录
date: 2023-12-06 23:24:09
description: 百抗校园网自动登录
---
# 需求
这几天要去出差，电脑在宿舍只要用了25G流量，无论是否还剩流量，都会被强制下线需要重新登录，所以需要检查能否联网然后登陆

而且最近selenium库有了一些大更新，最主要的就是查找网页元素的函数进行了修改，导致之前的程序都会报错，顺便做下之前文章的更新内容

但是夸奖一下校园网，他终于不是在url发get请求来登录了，进行了md5加密，导致我没法简单发requests请求来登录了
# selenium库更新
曾经查找元素的命令(以xpath查找为例)
```
from selenium import webdriver

driver.find_element_by_xpath('//*[@id="kw"]').send_keys('this is a test')
```
如今无论查找方式都是用一个函数，查找方式变成了第一个参数
```
from selenium import webdriver
from selenium.webdriver.common.by import By

driver.find_element(By.XPATH, "/html/body/main/section/div[1]/div[2]/input")
```
其他倒是都是一些小问题
# 自动登录程序
毕竟是校园网，我猜网页xpath短时间内都不会有变化hhh
```
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

username = "123456"
password = "654321"

while True:
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    try:
        requests.get(url='https://baidu.com/')
        print("Connected to the internet")
    except:
        try:
            print("Not connected to the internet, try to log in...")
            driver = webdriver.Edge()
            driver.minimize_window()
            driver.get("http://login.cumtb.edu.cn/")
            driver.find_element(By.XPATH, "/html/body/main/section/div[1]/div[2]/input").send_keys(username)
            driver.find_element(By.XPATH, "/html/body/main/section/div[1]/div[3]/input").send_keys(password)
            driver.find_element(By.XPATH, "/html/body/main/section/div[1]/div[5]/button").click()
            time.sleep(3)
            print('remain_flow：'+driver.find_element(By.XPATH, "/html/body/main/section/div[1]/div[5]/span[2]").text)
            driver.quit()
        except:
            print('Failed to log in.')
    time.sleep(60)

```
