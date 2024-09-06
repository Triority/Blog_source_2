---
title: windows创建文件软连接
tags:
  - windows
cover: /img/QQ截图20230204020745.png
categories:
- 折腾记录
notshow: false
date: 2023-02-04 02:08:32
description: mklink
---
想利用onedrive同步文件夹。但是onedrive的同步只能选择桌面等指定的几个文件夹。于是采用直接创建软连接到onedrive目录的方法：
```
mklink /D "F:\OneDrive - xxx\hexo" F:\hexo
```
注意是在cmd不是powershell，而且还需要管理员权限：
![注意是在cmd不是powershell](/img/QQ截图20230204020745.png)
