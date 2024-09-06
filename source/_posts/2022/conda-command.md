---
title: conda常用命令
date: 2022-10-22 00:25:35
tags:
- python
- 命令
description: conda常用命令
cover: /img/conda.png
categories: 
- 文档&笔记
---
## 下载及安装
```
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```
此时输入`conda`找不到命令，需要修改环境变量
```
source ~/.bashrc
```
## 相关命令
```
#创建名为py37的python3.7虚拟环境
conda create -n py37 python=3.7
#进入py37环境
conda activate py37
#安装python的ipython模块
conda install ipython
#退出当前环境
conda deactivate
#查看已安装的包
conda list
#删除虚拟环境
conda remove -n py37 --all
#查看当前存在哪些虚拟环境
conda env list 
```
## 更新环境
```
#检查更新当前conda
conda update conda
#更新anaconda
conda update anaconda
#更新所有库
conda update --all
#更新python
conda update python
```