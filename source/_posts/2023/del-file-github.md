---
title: 删除在github提交的敏感文件
cover: /img/RUN.png
categories:
- 折腾记录
date: 2023-09-29 12:22:38
description: 删除git仓库的一个文件及其全部历史记录
---
之前整个博客的源文件仓库是私有库，里面放了一些神奇的东西，密码密钥之类的，最近在想把这个仓库公开(贡献更多绿点)，所以需要删除之前提交的文件的全部历史记录

因为我要删除的文件很少，所以直接用一个git命令解决：

> 注意如果要删除记录的文件在仓库里，此操作将会删除这个文件，所以如果这个文件很重要务必备份

```
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch PATH-TO-YOUR-FILE-WITH-SENSITIVE-DATA' --prune-empty --tag-name-filter cat -- --all
```
本地仓库删除关于这个文件的全部记录之后，再强制推送到github覆盖github的提交记录：
```
git push --force
```

github文档里提供了一个删除文件的工具，但是还要下载就懒得弄了，但是放个[链接](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)