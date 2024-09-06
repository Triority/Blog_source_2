---
title: 部署hexo于远程服务器
date: 2022-12-26 22:52:37
tags:
- hexo
description: 换了新的但是配置差一些的服务器，主要是内存只有1G，如果继续在服务器本地hexo g会爆内存，所以改成在本地hexo g然后直接git push
cover: /img/hexo.png
categories: 
- 折腾记录
---
## 前言
以前一直在用腾讯云的学生服务器，终于还有两个月到期了。换了阿里云24r/月的香港轻量应用服务器，虽然价格便宜，但是内存只有1G，如果继续在服务器本地执行`hexo g`会爆内存，所以改成在本地`hexo g`然后直接git push到服务器上，而且本地编写文件比在宝塔面板上舒服多了
另外git push时候每次都需要输入服务器密码来ssh连接，让我十分不爽，所以直接让ssh用密钥登陆，再也不用输入密码了，这才叫优雅！
## 远程服务器部署
#### 安装服务器依赖–Git
```
apt install git-core -y
```
#### 配置环境
```
cd ~
mkdir hexo.git && cd hexo.git
git init --bare
```
```
nano /root/hexo.git/hooks/post-receive
```
```
#!/bin/bash
GIT_REPO=/root/hexo.git  #git仓库
TMP_GIT_CLONE=/tmp/hexo
PUBLIC_WWW=/hexo #网站目录
rm -rf ${TMP_GIT_CLONE}
git clone $GIT_REPO $TMP_GIT_CLONE
rm -rf ${PUBLIC_WWW}/*
cp -rf ${TMP_GIT_CLONE}/* ${PUBLIC_WWW}
```
赋予post-receive脚本的执行权限
```
cd /root/hexo.git/hooks
chmod +x post-receive
```
#### 修改nginx配置
直接上宝塔面板了
新建站点-填写域名和网站根目录-完成
## 本地配置
#### 安装hexo-deployer-git
```
npm install hexo-deployer-git --save
```
#### 配置文件
编辑`_config.yml`并修改`deploy`选项：
```
deploy:
  type: git
  message: update
  repo: root@IP:/root/hexo.git
  branch: master
```
## 提交
```
hexo d
```
## 优雅的hexo d
### 关闭Warn
使用hexo d时会出现大量警告，原因是在windows下换行符的问题，但是在编写amrkdown文件时无关紧要，可以直接关闭提示：
```
git config --global core.autocrlf false
```
### 密钥登陆
使用hexo d时会要求输入服务器密码，可以使用密钥登陆免除密码这一步骤。
以我现在的windows系统为例，ssh配置文件位于`C:\Users\Triority\.ssh`目录内
打开`config`文件，在其中添加：
```
Host www.triority.cn
    HostName www.triority.cn
    User triority
    IdentityFile C:\Users\Triority\www.triority.cn_id_123456
    IdentitiesOnly true
```
修改为你自己的域名，用户名，密钥文件路径。
如果你复制了密钥文件，可能出现权限过大拒绝使用这一密钥的情况，报错：
```
PS F:\> ssh -i .\www.triority.cn_id_ed25519 root@www.triority.cn
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions for '.\\www.triority.cn_id_ed25519' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
```
解决方法：
文件属性-安全-高级-禁用继承-删除所有已继承权限-添加-选择主体-输入用户名-确定-完全控制-确定-确定
即可使用密钥登陆：
```
ssh -i .\www.triority.cn_id_123456 root@www.triority.cn
```