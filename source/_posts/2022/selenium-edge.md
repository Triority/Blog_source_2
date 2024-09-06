---
title: python使用selenium操作edge浏览器
date: 2022-12-12 21:59:04
tags:
- python
description: python使用selenium操作edge浏览器
cover: /img/selenium.webp
categories: 
- 文档&笔记
---
## 安装所需文件
### python库
`pip install selenium
`
### edge浏览器驱动
查看浏览器版本链接`edge://settings/help`
[驱动下载网址](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ "下载网址")
选择跟自己浏览器版本一致的下载

### 将驱动程序放入指定目录
将下载好的驱动解压复制到Python安装目录下Scripts中，并将驱动`msedgedriver.exe`重命名为`MicrosoftWebDriver.exe`，文件名不对会导致调用不到。

### 简单测试
```python
from selenium import webdriver  # 引入模块
driver = webdriver.Edge()  # 引入edge驱动
driver.get("https://www.baidu.com/")  # 打开百度
```
## 基本操作
### 打开网页
`driver.get(url)`
比如刚才的测试例子。
### 元素定位方法
```python
find_element_by_id()
# html规定，id在html中必须是唯一的，有点类似于身份证号
find_element_by_name()
# html规定，name用来指定元素的名称，有点类似于人名
find_element_by_tag_name()
# 通过元素的签名来定位
find_element_by_class_name()
# html规定，class指定元素的类名
find_element_by_link_text()
# 专门用来定位文本链接
find_element_by_partial_link_text()
# 是对link_text的一种补充，有些文字链接比较长，可以取一部分链接文字进行定位，只要这部分文字是唯一标志这个链接的
find_element_by_css_selector()
find_element_by_xpath()
```
在`element`变成`elements`就是找所有满足的条件，返回数组。
### 控制浏览器操作
#### 控制浏览器窗口大小
```python
driver.set_window_size(480, 800)
```
#### 浏览器后退，前进，刷新
```python
driver.back()
driver.forward()
driver.refresh()
```
### 常用方法
#### 点击和输入
```python
driver.find_element_by_id("kw").clear() # 清除文本
driver.find_element_by_id("kw").send_keys("selenium") # 模拟按键输入
driver.find_element_by_id("su").click() # 单击元素
```
#### 提交
可以在搜索框模拟回车操作
```python
search_text = driver.find_element_by_id('kw')
search_text.send_keys('selenium') 
search_text.submit()
```
#### 其他
size： 返回元素的尺寸。
text： 获取元素的文本。
get_attribute(name)： 获得属性值。
is_displayed()： 设置该元素是否用户可见。

#### 鼠标操作
在 WebDriver 中， 将这些关于鼠标操作的方法封装在 ActionChains 类提供。
ActionChains 类提供了鼠标操作的常用方法：
```python
perform()# 执行所有 ActionChains 中存储的行为；
context_click()# 右击；
double_click(# 双击；
drag_and_drop()# 拖动；
move_to_element()# 鼠标悬停。
```
举个例子：
```python
from selenium import webdriver
# 引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Chrome()
driver.get("https://www.baidu.cn")
# 定位到要悬停的元素
above = driver.find_element_by_link_text("设置")
# 对定位到的元素执行鼠标悬停操作
ActionChains(driver).move_to_element(above).perform()
```
#### 键盘操作
```python
send_keys(Keys.BACK_SPACE) 删除键（BackSpace）
send_keys(Keys.SPACE) 空格键(Space)
send_keys(Keys.TAB) 制表键(Tab)
send_keys(Keys.ESCAPE) 回退键（Esc）
send_keys(Keys.ENTER) 回车键（Enter）
send_keys(Keys.CONTROL,'a') 全选（Ctrl+A）
send_keys(Keys.CONTROL,'c') 复制（Ctrl+C）
send_keys(Keys.CONTROL,'x') 剪切（Ctrl+X）
send_keys(Keys.CONTROL,'v') 粘贴（Ctrl+V）
send_keys(Keys.F1) 键盘 F1
```

```python
# 输入框输入内容
driver.find_element_by_id("kw").send_keys("seleniumm")
# 删除多输入的一个 m
driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE)
```
#### 获取断言信息
```python
title = driver.title # 打印当前页面title
now_url = driver.current_url # 打印当前页面URL
user = driver.find_element_by_class_name('nums').text # # 获取结果数目
```
#### 等待页面加载完成
##### 显示等待
显式等待使WebdDriver等待某个条件成立时继续执行，否则在达到最大时长时抛出超时异常（TimeoutException）。
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.baidu.com")

element = WebDriverWait(driver, 5, 0.5).until(
                      EC.presence_of_element_located((By.ID, "kw"))
                      )
element.send_keys('selenium')
driver.quit()
```
WebDriverWait类是由WebDirver 提供的等待方法。在设置时间内，默认每隔一段时间检测一次当前页面元素是否存在，如果超过设置时间检测不到则抛出异常。具体格式如下：
```python
WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)
```
driver ：浏览器驱动。
timeout ：最长超时时间，默认以秒为单位。
poll_frequency ：检测的间隔（步长）时间，默认为0.5S。
ignored_exceptions ：超时后的异常信息，默认情况下抛NoSuchElementException异常。
WebDriverWait()一般由until()或until_not()方法配合使用，下面是until()和until_not()方法的说明。
until(method, message=‘’) 调用该方法提供的驱动程序作为一个参数，直到返回值为True。
until_not(method, message=‘’) 调用该方法提供的驱动程序作为一个参数，直到返回值为False。
在本例中，通过as关键字将expected_conditions 重命名为EC，并调用presence_of_element_located()方法判断元素是否存在。
##### 隐式等待
如果某些元素不是立即可用的，隐式等待是告诉WebDriver去等待一定的时间后去查找元素。 默认等待时间是0秒，一旦设置该值，隐式等待是设置该WebDriver的实例的生命周期。

```python
from selenium import webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```
#### 警告框处理
```python
alert = driver.switch_to_alert()
```
text：返回 alert/confirm/prompt 中的文字信息。
accept()：接受现有警告框。
dismiss()：解散现有警告框。
send_keys(keysToSend)：发送文本至警告框。keysToSend：将文本发送至警告框。
#### 下拉框选择
```python
from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://www.baidu.com')
sel = driver.find_element_by_xpath("//select[@id='nr']")
Select(sel).select_by_value('50')  # 显示50条
```
#### 文件上传
```python
driver.find_element_by_name("file").send_keys('D:\\upload_file.txt')  # # 定位上传按钮，添加本地文件
```
#### cookie操作
WebDriver操作cookie的方法：

get_cookies()： 获得所有cookie信息。
get_cookie(name)： 返回字典的key为“name”的cookie信息。
add_cookie(cookie_dict) ： 添加cookie。“cookie_dict”指字典对象，必须有name 和value 值。
delete_cookie(name,optionsString)：删除cookie信息。“name”是要删除的cookie的名称，“optionsString”是该cookie的选项，目前支持的选项包括“路径”，“域”。
delete_all_cookies()： 删除所有cookie信息
#### 窗口截图
```python
driver.get_screenshot_as_file("D:\\baidu_img.jpg") # 截取当前窗口，并指定截图图片的保存位置
```
#### 关闭浏览器
close() 关闭单个窗口
quit() 关闭所有窗口
#### 直接用cookie登录方法
链接：https://www.jianshu.com/p/773c58406bdb
手动获取网页的cookie，将其序列化并存储在本地
```python
for item in cookies:
    driver.add_cookie(item)
```
## 注意
这篇文章的内容绝大多数是从网络上复制而来，没有经过实践验证，而且实测的几个基本都跑不通，只是留着给以后挖坑，不具有参考价值