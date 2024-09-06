---
title: hexo博客文章特殊md代码记录
date: 2022-07-01 17:21:27
tags:
- hexo
- 笔记
description: 编写博客过程中需要的特殊代码永远记不住...用一次查一次...于是：
cover: /img/hexo-post-code.webp
categories: 
- 文档&笔记
---
### 文章分类
```
- 值得一提的文章
- 做点好玩的
- [计算机, CV工程师]
- [计算机, 源码分享]
- [计算机, 知识整理]
- [计算机, 折腾记录]
- [计算机, 文档教程]
- [生活, 游览记录]
- [生活, 天文摄影]
- [生活, 摄影合辑]
- 整活
- minecraft
```
### 插入图片：
```
//插件：
{% asset_img xxx.png 描述 %}
//Markdown：
![描述](xxx.png)
```

### 插入视频：
```
{% dplayer "url=wwww.xxx.cn/xxx.mp4" %}
{% dplayer "url=/video/xxx.mp4" %}
```

### 文件下载链接：
```
[文字](xxx.zip "描述")
```
### 哔哩哔哩视频：
需要替换的内容：`src`
```
{% raw %}
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
<iframe src="//player.bilibili.com/player.html?aid=727587109&bvid=BV1LS4y1v7Nj&cid=748560556&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="position: absolute; width: 100%; height: 100%; Left: 0; top: 0;" ></iframe></div>
{% endraw %}
```
### 折叠代码
```
<details>
  <summary>点击时的区域标题</summary>
  xxx
</details>
```

### 小黑块：
```
{% spoiler 被遮挡文字 %}
```
