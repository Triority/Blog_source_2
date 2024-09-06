---
title: butterfly配置
tags:
  - hexo
cover: https://file.crazywong.com/gh/jerryc127/butterfly_cdn@2.1.0/top_img/index.jpg
categories:
- 文档&笔记
notshow: false
date: 2023-06-07 09:35:07
description: butterfly配置
---
# 前言
之前用的fluid主题，心血来潮换成了butterfly，感觉还不错，不过可配置项就会多出很多，官方文档虽然全面但是顺序有点乱七八糟不好找，所以按自己的顺序写一些经常用到的配置项
# 页面
## 主图片
[顶部图](https://butterfly.js.org/posts/4aa8abbe/#%E9%A0%82%E9%83%A8%E5%9C%96)

[文章封面](https://butterfly.js.org/posts/4aa8abbe/#%E6%96%87%E7%AB%A0%E5%B0%81%E9%9D%A2)

[主页图片大小配置](https://butterfly.js.org/posts/ceeb73f/#%E4%B8%BB%E9%A0%81top-img%E9%A1%AF%E7%A4%BA%E5%A4%A7%E5%B0%8F)

## 主页
[网站背景](https://butterfly.js.org/posts/ceeb73f/#%E7%B6%B2%E7%AB%99%E8%83%8C%E6%99%AF)

[副标题](https://butterfly.js.org/posts/ceeb73f/#%E7%B6%B2%E7%AB%99%E5%89%AF%E6%A8%99%E9%A1%8C)

[页面加载动画](https://butterfly.js.org/posts/ceeb73f/#%E9%A0%81%E9%9D%A2%E5%8A%A0%E8%BC%89%E5%8B%95%E7%95%AB-preloader)

## 侧边栏
[侧边排版](https://butterfly.js.org/posts/4aa8abbe/#%E5%81%B4%E9%82%8A%E6%AC%84%E8%A8%AD%E7%BD%AE-aside)

## 导航栏-Navigation bar

[导航栏设置](https://butterfly.js.org/posts/4aa8abbe/#%E5%B0%8E%E8%88%AA%E6%AC%84%E8%A8%AD%E7%BD%AE-Navigation-bar-settings)

## 底部
[页脚自定义文本](https://butterfly.js.org/posts/4aa8abbe/#%E9%A0%81%E8%85%B3%E8%87%AA%E5%AE%9A%E7%BE%A9%E6%96%87%E6%9C%AC)

## Front-matter

| 写法   | 解释   |
|--------|--------|
|title|	【必需】页面标题|
|date	|【必需】页面创建日期|
|type	|【必需】标签、分类和友情链接三个页面需要配置|
|updated	|【可选】页面更新日期|
|description	|【可选】页面描述|
|keywords	|【可选】页面关键字|
|comments|	【可选】显示页面评论模块 (默认 true)|
|top_img	|【可选】页面顶部图片|
|mathjax|	【可选】显示mathjax (当设置mathjax的per_page: false时，才需要配置，默认 false)|
|katex	|【可选】显示katex (当设置katex的per_page: false时，才需要配置，默认 false)|
|aside	|【可选】显示侧边栏 (默认 true)|
|aplayer	|【可选】在需要的页面加载aplayer的js和css,请参考文章下面的音乐 配置|
|highlight_shrink	|【可选】配置代码框是否展开 (true/false) (默认为设置中highlight_shrink的配置)|
|random	|【可选】配置友情链接是否随机排序（默认为 false)|

# 文章
## Front-matter

| 写法   | 解释   |
|--------|--------|
|title	|【必需】文章标题|
|date	|【必需】文章创建日期|
|updated|	【可选】文章更新日期|
|tags	|【可选】文章标签|
|categories	|【可选】文章分类|
|keywords	|【可选】文章关键字|
|description	|【可选】文章描述|
|top_img	|【可选】文章顶部图片|
|cover	|【可选】文章缩略图(如果没有设置top_img,文章页顶部将显示缩略图，可设为false/图片地址/留空)|
|comments	|【可选】显示文章评论模块(默认 true)|
|toc	|【可选】显示文章TOC(默认为设置中toc的enable配置)|
|toc_number	|【可选】显示toc_number(默认为设置中toc的number配置)|
|toc_style_simple|	【可选】显示 toc 简洁模式|
|copyright	|【可选】显示文章版权模块(默认为设置中post_copyright的enable配置)|
|copyright_author	|【可选】文章版权模块的文章作者|
|copyright_author_href	|【可选】文章版权模块的文章作者链接|
|copyright_url	|【可选】文章版权模块的文章连结链接|
|copyright_info	|【可选】文章版权模块的版权声明文字|
|mathjax|	【可选】显示mathjax(当设置 mathjax 的 per_page: false 时，才需要配置，默认 false )|
|katex	|【可选】显示 katex (当设置 katex 的 per_page: false 时，才需要配置，默认 false )|
|aplayer	|【可选】在需要的页面加载 aplayer 的 js 和 css,请参考文章下面的音乐 配置|
|highlight_shrink|	【可选】配置代码框是否展开(true/false)(默认为设置中 highlight_shrink 的配置)|
|aside	|【可选】显示侧边栏 (默认 true)|
|abcjs	|【可选】加载 abcjs (当设置 abcjs 的 per_page: false 时，才需要配置，默认 false )|

## 特殊语法(Note/相册/按钮/流程图/Tabs/timeline/乐谱/链接界面)
[标签外挂（Tag Plugins）](https://butterfly.js.org/posts/4aa8abbe/#%E6%A8%99%E7%B1%A4%E5%A4%96%E6%8E%9B%EF%BC%88Tag-Plugins%EF%BC%89)

# 其他
## 友链
友情链接随机排序只需要在顶部 `front-matter` 添加 `·random: true`

```
    - name: Twitter
      link: https://twitter.com/
      avatar: https://i.loli.net/2020/05/14/5VyHPQqR6LWF39a.png
      descr: 社交分享平台
```
## 图库
[图库官方文档](https://butterfly.js.org/posts/dc584b87/#%E5%9C%96%E5%BA%AB)

## 音乐

## 代码
[代码(Code Blocks)](https://butterfly.js.org/posts/4aa8abbe/#%E4%BB%A3%E7%A2%BC-Code-Blocks)

## 社交图标
[font-awesome v6 图标](https://fontawesome.com/icons?from=io)

[社交图标文档](https://butterfly.js.org/posts/4aa8abbe/#%E7%A4%BE%E4%BA%A4%E5%9C%96%E6%A8%99-Social-Settings)

```
social:
  fab fa-github: https://github.com/xxxxx || Github || "#hdhfbb"
  fas fa-envelope: mailto:xxxxxx@gmail.com || Email || "#000000"
```
