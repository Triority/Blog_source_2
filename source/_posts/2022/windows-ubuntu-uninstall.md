---
title: windows-ubuntu双系统卸载ubuntu
date: 2022-07-15 23:58:42
tags:
- linux
- 教程
description: 卸载ubuntu系统
cover: /img/win_ubuntu_uninstall.png
categories: 
- 折腾记录
---
## 前言
半年前安装的Windows+ubuntu18双系统，由于当时硬盘空间紧张，所以只分配了20G挂载在"/"以及20G挂载在"/home"，经过半年的使用，ubuntu的存储空间已经耗尽，所以打算重装来重新分配空间

## 删除ubuntu分区
首先，在windows系统下，删除ubuntu的系统分区，我在安装时分区有4个，efi系统分区，两个日志文件分区以及一个交换空间分区，按下ctrl+x，选择磁盘管理，以上全部在磁盘管理中删除。由于efi分区是系统分区，windows不允许删除，可以先留着~~[活得过初一躲不过十五]~~。
![是我完成重装后截的图](1.png)
## 删除ubuntu系统引导
### 打开被隐藏的启动项分区
win+R打开运行，输入：
```
diskpart
```
回车打开命令行，命令行内输入以下，即可看到全部磁盘：
```
list disk
```
![全部磁盘](2.png)



选择Windows的安装磁盘，启动项一般都是在磁盘0，选中这个磁盘：
```
select disk 0
```
![选中磁盘](3.png)



查看该磁盘的分区信息：
```
list partition
```
![分区信息](4.png)



确定Windows的EFI分区，一般是200M左右，我这里是分区1，选中这个分区：
```
select partition 1
```
![选中分区](5.png)



为它分配盘符，盘符不可与已有盘符重复，所以我写的是J
```
assign letter=J
```
![分配盘符](6.png)



此时在资源管理器的我的电脑就可以看到新的J盘，但是由于权限不够无法打开
网上许多教程都写的是通过记事本间接打开，但是我实际操作时没有成功，一旦开始文件操作就会让记事本无响应，不知道与我的操作系统是win11有关
这里讲我的。首先用管理员权限打开powershell



然后cd进入J盘
```
cd J:\
```
通过ls可以看到磁盘里的内容
![J盘内容](7.png)
然后进入这个文件夹
```
cd EFI
```
继续ls查看内容
![EFI文件夹内容](8.png)



这里有一个ubuntu文件夹，这就是ubuntu的系统引导，把他删除
```
Remove-Item 'ubuntu'
```
会有一个确认操作，输入Y确认。
可以通过ls确认文件已经删除
![删除完成](9.png)

继续隐藏启动分区：
```
remove letter=J
```
![隐藏分区](10.png)


## 完成
注：由于我使用rEFInd引导系统启动，所以没有在BIOS中修改系统引导优先级[我觉得就算没安装也可以不改]
此时ubuntu已经完全卸载，可重启电脑，进行安装ubuntu双系统的操作

## ubuntu双系统的安装
ubuntu双系统的安装推荐这一篇文章：
[安装windows+ubuntu双系统教程](https://blog.csdn.net/jiqirenX/article/details/72367905 "安装windows+ubuntu双系统教程")