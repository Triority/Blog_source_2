---
title: Capoo-Desktop-Pet：使用PyQT开发桌宠程序并打包为windows软件
date: 2022-12-07 15:38:24
tags:
- python
- Qt
description: 使用PyQT开发桌宠程序并打包为windows软件
cover: /img/Capoo.jpg
categories: 
- [折腾记录]
- [作品&项目总结]
- [值得一提的文章]
---
## 前言
之前在b站刷到了Capoo的视频，这猫猫也太好玩了哈哈，最近原作者做了一个桌宠app，但是付款方式只有paypel(据说价格挺贵)，so自己搓一个？
![效果图](capoodesktoppet.png)
## PyQt5编写程序
虽然说一般python不适合写这类应用程序，但是以我C的能力还是算了hhh
### 目录结构

Capoo
└ normal
.    └ normal1.gif
.    └ normal2.gif
.    └ normal3.gif
.    └ normal4.gif
.    └..............
└ click
.    └ click.gif
└ main.py
└ dialog.txt
└ tigerIcon.jpg

注释：
`normal`文件夹包含需要随机显示的全部图片，程序启动时首先打开的是`normal1.gif`，其他文件名随意，建议图片设置透明背景
`click.gif`是点击时显示的图片
`main.py`主程序
`dialog.txt`多行文本，随机显示的话，编码格式为GBK
`tigerIcon.jpg`状态栏显示的图标

### python程序
`main.py`
```python
import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initPall()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()

    # 窗体初始化
    def init(self):
        # 初始化
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        # https://blog.csdn.net/kaida1234/article/details/79863146
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 重绘组件、刷新
        self.repaint()

    # 托盘化设置初始化
    def initPall(self):
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('tigerIcon.jpg')
        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置这个点击选项的图片
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.showwin)
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

    # 宠物静态gif图加载
    def initPetImage(self):
        # 对话框定义
        self.talkLabel = QLabel(self)
        # 对话框样式设计
        self.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")
        # 定义显示图片部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        self.movie = QMovie("normal/normal1.gif")
        # 设置标签大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(1024, 1024)
        # 调用自定义的randomPosition，会使得宠物出现位置随机
        self.randomPosition()
        # 展示
        self.show()
        # 将宠物正常待机状态的动图放入pet1中
        self.pet1 = []
        for i in os.listdir("normal"):
            self.pet1.append("normal/" + i)
        # 将宠物正常待机状态的对话放入pet2中
        self.dialog = []
        # 读取目录下dialog文件
        with open("dialog.txt", "r") as f:
            text = f.read()
            # 以\n 即换行符为分隔符，分割放进dialog中
            self.dialog = text.split("\n")

    # 宠物正常待机动作
    def petNormalAction(self):
        # 每隔一段时间做个动作
        # 定时器设置
        self.timer = QTimer()
        # 时间到了自动执行
        self.timer.timeout.connect(self.randomAct)
        # 动作时间切换设置
        self.timer.start(3000)
        # 宠物状态设置为正常
        self.condition = 0
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(3000)
        # 对话状态设置为常态
        self.talk_condition = 0
        # 宠物对话框
        self.talk()

    # 随机动作切换
    def randomAct(self):
        # condition记录宠物状态，宠物状态为0时，代表正常待机
        if not self.condition:
            # 随机选择装载在pet1里面的gif图进行展示，实现随机切换
            self.movie = QMovie(random.choice(self.pet1))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
        # condition不为0，转为切换特有的动作，实现宠物的点击反馈
        else:
            # 读取特殊状态图片路径
            self.movie = QMovie("./click/click.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0
            self.talk_condition = 0

    # 宠物对话框行为处理
    def talk(self):
        if not self.talk_condition:
            # talk_condition为0则选取加载在dialog中的语句
            self.talkLabel.setText(random.choice(self.dialog))
            # 设置样式
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            # 根据内容自适应大小
            self.talkLabel.adjustSize()
        else:
            # talk_condition为1显示为别点我，这里同样可以通过if-else-if来拓展对应的行为
            self.talkLabel.setText("别摸我")
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
            # 设置为正常状态
            self.talk_condition = 0

    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()

    # 显示宠物
    def showwin(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        self.setWindowOpacity(1)

    # 宠物随机位置
    def randomPosition(self):
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen_geo = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        # 更改宠物状态为点击
        self.condition = 1
        # 更改宠物对话状态
        self.talk_condition = 1
        # 即可调用对话状态改变
        self.talk()
        # 即刻加载宠物点击动画
        self.randomAct()
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.OpenHandCursor))

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        # 定义菜单项
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == quitAction:
            qApp.quit()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)


if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = DesktopPet()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())

```
## pyinstaller将程序打包为exe
```python
pyinstaller -F -w main.py
```
打包生成的`main.exe`放到主目录下
## 制作安装程序
刚才打包为exe后是一个文件夹，分享给他人后需要解压之后启动main.exe，可是如果，我是说如果，你有一个女朋友，但是她连解压都不会，so最好做成一个`Setup.exe`，打开连点下一步，安装之后直接一个桌面快捷方式，那该多好。
![安装程序](安装程序图.png)
### 安装环境
1.`Nullsoft Inst all System(NSIS)`：编译 .nsi脚本文件，生成Setup.exe
2.`VNISEdit`：生成 .nsi脚本文件
注意，如果没有安装NSIS直接打开VNISEdit，会在选择语言一步卡死，因为候选栏为空。
下载链接：
[VNISEdit.rar](VNISEdit.rar)
[nsis-3.02.1-setup.exe](nsis-3.02.1-setup.exe)
### 生成 .nsi脚本文件
1.打开VNISEdit
选择：文件->新建脚本：向导
![向导](20221207163210.png)
2.填写应用程序信息
![应用程序信息](20221207163234.png)
3.填写安装程序选项
![安装程序选项](20221207163254.png)
4.设置快闪屏幕和背景窗口。花里胡哨的，我直接下一步
5.应用程序的目录和授权信息
没有授权文件的话，需要把输入框清空，再下一步
![应用程序的目录和授权信息](20221207163311.png)
6.应用程序文件
先删除右边框子里所有的默认文件，然后点击添加目录树
一定要勾选上下面两个复选框
![应用程序文件](20221207163354.png)
7.应用程序图标
记得准备一个ico格式的图标哦
8.安装程序之后运行
选择我们的主程序，也就是`main.exe`
![主程序](20221207163418.png)
9.解除安装程序，不用改
10.保存脚本
一定要勾选上前两个复选框
![保存](20221207163427.png)
### 编译 .nsi脚本
打开Nullsoft Inst all System(NSIS)
选择第一个编译nsi
![编译nsi](20221207163546.png)
把之前生成的nsi文件推进去，等他编译完，就大功告成咯
## 下载链接
安装程序：
[CapooSetup.exe](https://cr.triority.cn/f/vZhl/CapooSetup.exe)
python编译exe文件：
[main.exe](https://cr.triority.cn/f/qYFA/main.exe)
