---
title: 博客github仓库通过action自动化部署
tags:
  - hexo
cover: /img/RUN.png
categories:
  - 折腾记录
date: 2024-09-06 16:49:18
description: 目前找到的博客部署最优解
---
# 方案比较
之前的部署方案是服务器本地保存源文件，写入新内容时使用vscode的远程ssh编辑，然后git推送到github仓库作为备份。有一点问题就是服务器硬件来自阿里云的轻量应用服务器，对硬盘的iops有限制，进行大量读写操作时候一旦超过就会引发系统死机。以及稀烂的CPU和内存资源，随着源文件越来越大，生成时间也越来越长。这个时候github推出了action功能，允许我直接在github的服务器上进行生成操作，而且速度掉打阿里云服务器。所以方案改成这样，直接使用github保存源代码，每次提交代码之后自动进行生成操作，同时将生成的静态文件直接通过git推送到服务器的网站服务目录内。同时也简化了另一个问题，就是多用户编辑，之前需要服务器上多个用户的读写权限，现在只需要授权github仓库就可以了。

# hexo部署推送
也就是执行`hexo d`之后将生成的代码通过git推送到自己的远程服务器，这部分内容我在2022年写过，因为当时的方案是本地编辑生成然后git推送到服务器，和现在一样，直接参考[这篇文章](https://triority.cc/2022/remote-server-hexo/)

# github action配置
github开了一个新的仓库保存源代码，上传现有内容之后，准备新建action。`GitHub Actions`的配置文件叫做`workflow`文件，存放在源代码仓库的`.github/workflows`目录。GitHub在我们完成预设触发条件时，只要发现`.github/workflows`目录里面有`.yml`文件，就会自动读取运行该文件。

## 编辑workflow
```
name: Blog CI/CD

on:
  push:
    branches: [main] # 当监测 main,master 的 push
    paths: # 监测文件变动限制
      - '*.json'
      - '**.yml'
      - '**.md'
      - '**/source/**'

jobs:
  blog: # 任务名称
    timeout-minutes: 10 # 设置 10 分钟超时
    runs-on: ubuntu-latest # 指定最新 ubuntu 系统
    steps:
      - uses: actions/checkout@v2 # 拉取仓库代码
      - uses: actions/setup-node@v2 # 设置 node.js 环境
      - name: Cache node_modules # 缓存 node_modules，提高编译速度，毕竟每月只有 2000 分钟。
        uses: actions/cache@v2
        env:
          cache-name: cache-node-modules
        with:
          path: ~/.npm
          key: ${{ runner.os }}-build-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ env.cache-name }}-
            ${{ runner.os }}-build-
            ${{ runner.os }}-
      - name: Init Node.js # 安装源代码所需插件
        run: |
          npm install
          echo "init node successful"
      - name: Install Hexo-cli # 安装 Hexo
        run: |
          npm install -g hexo-cli --save
          echo "install hexo successful"
      - name: Build # 编译创建静态博客文件
        run: |
          hexo clean
          hexo g
          echo "build blog successful"
      - name: Deploy # 设置 git 信息并推送静态博客文件
        uses: easingthemes/ssh-deploy@v2.1.1
        env:
          # 私钥id_rsa，存在secrets的PRIVATE_KEY中
          SSH_PRIVATE_KEY: ${{ secrets.PRIVATE_KEY }}
          # 复制操作参数，"-avzr --delete"部署时清空服务器目标目录下的文件
          ARGS: "-avzr --delete" 
          # 源目录，相对于$GITHUB_WORKSPACE根目录的路径
          SOURCE: "public/"
          REMOTE_HOST: "www.triority.cc"
          REMOTE_USER: "root"
          # 目标目录
          TARGET: "/blog_public"

      - run: echo "Deploy Successful!"
```
然后在仓库设置密钥`PRIVATE_KEY`值为ssh私钥文件即可
