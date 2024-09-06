---
title: ubuntu下使用rclone将onedrive挂载
tags:
  - linux
cover: /img/QQ截图20230120162127.png
categories:
- 折腾记录
notshow: false
date: 2023-01-20 15:41:17
description: ubuntu下使用rclone将onedrive挂载
---
## 前言
最近买了`onedrive`5T的容量，挂载给服务器岂不是巨香

网络上大部分教程都是使用vnc登录，由于我的服务器是ubuntu-server所以无法使用web登录onedrive。

## 下载rclone
[rclone](https://rclone.org/downloads/)：下载windows和deb两个。

## windows下获取token
解压windows版本的rclone，打开cmd：
```
rclone authorize "onedrive"
```
浏览器会跳转打开onedrive的登录页面，这一步是在手动获取access_token 将返回内容保存下来。

## 在ubuntu服务器上安装并配置
```
dpkg -i *.deb
```
```
rclone config
```
按n选择新建：
```
root@iZj6c9vpc0x2q5gkwla1erZ:~# rclone config
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n

Enter name for new remote.
name> triority

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
```
在巨长的列表里找到`onedrive`然后输入前面的序号，比如我是`31`：
```
29 / Mega
   \ (mega)
30 / Microsoft Azure Blob Storage
   \ (azureblob)
31 / Microsoft OneDrive
   \ (onedrive)
32 / OpenDrive
   \ (opendrive)
```
下面的`client id`和`client secret`直接回车跳过，默认留空：
```
Storage> 31

Option client_id.
OAuth Client Id.
Leave blank normally.
Enter a value. Press Enter to leave empty.
client_id>

Option client_secret.
OAuth Client Secret.
Leave blank normally.
Enter a value. Press Enter to leave empty.
client_secret>

Option region.
```
后面的地区按照实际情况选择：
```
Choose national cloud region for OneDrive.
Choose a number from below, or type in your own string value.
Press Enter for the default (global).
 1 / Microsoft Cloud Global
   \ (global)
 2 / Microsoft Cloud for US Government
   \ (us)
 3 / Microsoft Cloud Germany
   \ (de)
 4 / Azure and Office 365 operated by Vnet Group in China
   \ (cn)
region> 4
```
然后选择配置，按照我们的需求两个都是`no`：
```
Edit advanced config?
y) Yes
n) No (default)
y/n> n

Use web browser to automatically authenticate rclone with remote?
 * Say Y if the machine running rclone has a web browser you can use
 * Say N if running rclone on a (remote) machine without web browser access
If not sure try Y. If Y failed, try N.

y) Yes (default)
n) No
y/n> n

Option config_token.
For this to work, you will need rclone available on a machine that has
a web browser available.
For more help and alternate methods see: https://rclone.org/remote_setup/
Execute the following on the machine with the web browser (same rclone
version recommended):
        rclone authorize "onedrive" "eyJyZWdpb24iOiJjbiJ9"
Then paste the result.
Enter a value.
config_token>
```
在这里输入刚才在windows下获取的`token`。然后按实际情况选择1：
```
Option config_type.
Type of connection
Choose a number from below, or type in an existing string value.
Press Enter for the default (onedrive).
 1 / OneDrive Personal or Business
   \ (onedrive)
 2 / Root Sharepoint site
   \ (sharepoint)
   / Sharepoint site name or URL
 3 | E.g. mysite or https://contoso.sharepoint.com/sites/mysite
   \ (url)
 4 / Search for a Sharepoint site
   \ (search)
 5 / Type in driveID (advanced)
   \ (driveid)
 6 / Type in SiteID (advanced)
   \ (siteid)
   / Sharepoint server-relative path (advanced)
 7 | E.g. /teams/hr
   \ (path)
config_type> 1
```
根据个人情况选是否挂载根目录,我选是，然后确认配置文件，选择默认即可。创建成功：
```
Keep this "triority" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y

Current remotes:

Name                 Type
====                 ====
triority             onedrive
```
## 查看和挂载
#### 查看能否读取
```
rclone lsd triority:/
```

```
root@iZj6c9vpc0x2q5gkwla1erZ:~# rclone lsd triority:/
          -1 2023-01-19 15:07:17         0 Code
```

#### 挂载硬盘
命令模板：
```
rclone mount DriveName:Folder LocalFolder --copy-links --no-gzip-encoding --no-check-certificate --allow-other --allow-non-empty --umask 000
```
> DriveName为初始化配置填的name，Folder为OneDrive里的文件夹，LocalFolder为服务器上的本地文件夹。

我的配置:
```
rclone mount triority:/ /onedrive --copy-links --no-gzip-encoding --no-check-certificate --allow-other --allow-non-empty --umask 000
```
因为是临时启动，打开另一个ssh 然后查看下后台挂载情况，挂载正常。
然后就可以使用`screen`持续运行了