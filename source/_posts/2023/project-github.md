---
title: 在工程中将代码提交至github
cover: /img/v2-4dccef85028e88d0d69f082d03dc2d09_1440w.jpg
categories:
- 折腾记录
notshow: false
date: 2023-04-16 19:26:10
description: 将自己的工程记录到github
---
# 创建github仓库
这部分不详细说了十分简单，在github仓库创建完成后还会给你显示常用命令
```
git init //把这个目录变成Git可以管理的仓库
git add README.md //文件添加到仓库
git add . //不但可以跟单一文件，还可以跟通配符，更可以跟目录。一个点就把当前目录下所有未追踪的文件全部add了 
git commit -m "first commit" //把文件提交到仓库
git remote add origin git@github.com:wangjiax9/practice.git //关联远程仓库
git push -u origin master //把本地库的所有内容推送到远程库上
```
# git安装

以windows系统为例，首先是欢迎界面，直接点击下一步

然后是安装路径，反正别带中文

然后选择安装组件：

![](安装组件.png)

+ 图标组件(Addition icons) : 选择是否创建快速启动栏图标 或者 是否创建桌面快捷方式
+ 桌面浏览(Windows Explorer integration) : 浏览源码的方法, 单独的上下文浏览 只使用bash 或者 只用Git GUI工具; 高级的上下文浏览方法 使用git-cheetah plugin插件
+ 关联配置文件(Associate .git*) : 是否关联git配置文件, 该配置文件主要显示文本编辑器的样式
+ 关联shell脚本文件(Associate .sh) : 是否关联Bash命令行执行的脚本文件
+ 使用TrueType编码 : 在命令行中是否使用TruthType编码

设置开始菜单中快捷方式的目录名称，默认就好

设置编辑器，反正我是习惯vscode

设置新仓库的分支名称，让git决定就好

选择使用什么样的命令行工具, 我一般选用第二个

![](命令行.png)

+ Git自带 : 使用Git自带的Git Bash命令行工具
+ 统自带CMD : 使用Windows系统的命令行工具
+ 二者都有 : 上面二者同时配置, 但是注意, 这样会将windows中的find.exe 和 sort.exe工具覆盖, 如果不懂这些尽量不要选择

选择ssh和https配置，默认就好

选择换行格式 ，依然是默认就好

![](换行格式.png)

+ 检查出windows格式转换为unix格式 : 将windows格式的换行转为unix格式的换行在进行提交
+ 检查出原来格式转为unix格式 : 不管什么格式的, 一律转为unix格式的换行在进行提交
+ 不进行格式转换 : 不进行转换, 检查出什么, 就提交什么

选择终端模拟器，依然默认就好

+ 用MinTTY，就是在Windows开了一个简单模拟Linux命令环境的窗口Git Bash
+ 使用windows的系统的命令行程序cmd.exe

下一个`git pull`行为以及后面的一般用不到，都是默认就好

安装完成

# git配置
### 创建标识
打开`git-bash.exe`，需要填写用户名和邮箱作为一个标识，用户和邮箱为你github注册的账号和邮箱
### 为Github账户设置SSH key
检查是否已生成密钥
```
cd ~/.ssh
ls
```
如果有2个文件，则密钥已经生成，`id_rsa.pub`就是公钥

如果没有生成，那么通过这个命令来生成
```
ssh-keygen -t rsa -C "xxxxxx@xxx.com"
```
然后路经确认默认即可，密码可以直接回车跳过

### 为github账号配置ssh key
切换到github，点击`settings`，打开`SSH keys`菜单， 点击`Add SSH key`新增密钥，将`id_rsa.pub`文件中`key`粘贴到此，最后`Add key`生成密钥，github账号的SSH keys配置完成

# 上传本地项目到github
## 使用命令行
### 建立本地仓库
这些命令的含义在开始就写过了
```
git init
git add .
git commit -m "提交注释"
git remote add origin git@github.com:xxx/xxx.git
git push -u origin master
```
最后一个命令报错可以尝试一下这个
```
git push -u origin master -f
```
## 使用pycharm
### pycharm上传配置
打开File—–settings，选择`Version Control`中的`github`并登录你的账号

再打开`github`选项上面的`git`选项，设置git路径，一般自动选择就好

上传代码VCS——Import inti Version Control——–Share Project on GitHub，输入仓库名称，是否私有，远程名称(默认即可)，以及描述，就可以选择文件然后上传了

以后再做修改，就可以直接选择右上角的`commit`(ctrl+k)和`push`

## 使用vscode
虽然vscde自带git插件，可以进行可视化操作，当然命令行也可以

首先在左侧源代码管理中，初始化仓库，并登录github，选择远程仓库之后就可以了

当做出修改时，在源代码管理界面，选择提交和同步，在弹出对话框中选择确定(可以选择始终)，然后vscode就会打开有个文件，在文件第一行写提交说明，然后保存并关掉这个文件，会弹出有个对话框来确认，同样，可以选择始终(OK,but don`t show again)，就可以提交到github了