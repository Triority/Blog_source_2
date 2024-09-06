---
title: windows下bitlocker加密盘快速锁定
tags:
  - windows
cover: /img/OIP-C.jpg
categories:
  - 折腾记录
date: 2023-10-03 17:58:19
description: bitlocker不用重启的锁定
---
# 快速锁定
首先如何使用bitlocker加密就不用说了吧

但是平时重启并解锁以后想要再次锁定很麻烦，一般要重启电脑，很麻烦。但是可以用命令行直接锁定
在这里我要锁定的磁盘是E盘：
```
manage-bde -lock E:
```
可以把这个命令写进cmd保存在E盘，用完直接运行cmd锁定

但是这样还需要cmd以管理员身份运行，可以设置cmd默认使用管理员权限运行：
# 默认管理员身份运行
## 还是这个方法好用
给cmd创建快捷方式，在快捷方式的属性中选择高级中的管理员权限，简单好用

## 这个有点复杂hhh而且实测好似不能用
```
作者：落梧
链接：https://www.zhihu.com/question/34541107/answer/154430381
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

@echo off
title 获取管理员权限
mode con cols=100 lines=20
color 3f

:: 开始获取管理员权限
setlocal
set uac=~uac_permission_tmp_%random%
md "%SystemRoot%\system32\%uac%" 2>nul
if %errorlevel%==0 ( rd "%SystemRoot%\system32\%uac%" >nul 2>nul ) else (
    echo set uac = CreateObject^("Shell.Application"^)>"%temp%\%uac%.vbs"
    echo uac.ShellExecute "%~s0","","","runas",1 >>"%temp%\%uac%.vbs"
    echo WScript.Quit >>"%temp%\%uac%.vbs"
    "%temp%\%uac%.vbs" /f
    del /f /q "%temp%\%uac%.vbs" & exit )
endlocal
:: 完成获取,下面可以开始写你自己的代码了

echo.
echo 原理：先尝试在系统目录下临时新建一个文件夹，若已获取管理员权限或是运行在XP等不需要管理员权限的
echo       老系统时，是可以新建成功的，此时只需删除这个临时新建的文件夹就好了，否则通过创建一个临时
echo       vbs脚本获取管理员权限，然后再删除这个临时vbs脚本文件。
echo.
echo 提示：当获取管理员目录后，你的批处理运行目录会发生变化，为保证目录准确，
echo       可通过 cd 切换目录,例“cd /d %%~dp0”切换回批处理所在目录
echo.
echo 当前运行目录： %cd%\
echo 批处理所在目录：%~dp0
echo.
echo 例：切换回批处理所在目录
echo cd /d %%~dp0
echo.

cd /d %~dp0

echo 当前运行目录： %cd%\
echo 批处理所在目录：%~dp0	

pause
exit
```


## 这个好似不管用hhh
在开始菜单中搜索cmd打开文件所在位置，右键属性，在高级中选择使用管理员权限运行，还可以设置默认打开最小化，更加优雅

![](QQ截图20231003180910.png)


