---
title: 博客文章编辑发布指南
tags:
  - hexo
  - 文档
cover: /img/d7534a8ee77467263a270461f030945.jpg
categories:
  - 文档&笔记
date: 2024-07-22 18:33:41
description: 博客帮助文件
---
# 概述
博客采用静态hexo框架，基于node js，文章使用markdown语言进行编写。源文件保存于github仓库，使用git进行源码管理，使用github action自动化部署到远程服务器，并使用nginx提供对外服务。
# 编辑权限
可以私信我或发邮件申请仓库编辑权限，或者直接在github仓库发起合并请求

# 新建和编辑文章
+ `git clone`下载github仓库源代码到本地
+ 编辑文件内容或使用`hexo new [name]`新建一个web链接为name的文章，新建的文章保存为`/hexo/source/[year]/[name].md`，即可在其中使用markdown语言编写文章
+ 提交你的更改并同步到github仓库
+ github action自动进行网站内容的生成和部署，等待三五分钟左右即可打开网站查看更改。如果`build`出现报错`err: Error: ENOENT: no such file or directory, open './search.xml'`请直接重试，仍然报错基本上markdown语法错误，请再次检查你的更改

# 文章配置
```md
---
title: [name]
tags:
  - null
cover: /img/RUN.png
categories:
  - - 值得一提的文章
  - - 旅游&摄影
  - - 日记本
  - - 整活&游戏
  - - 文档&笔记
  - - 折腾记录
  - - 作品&项目总结
  - - 过时&弃用&无意义&失败品
  - - 外部引用
  - - 无线电
date: 2024-07-22 18:44:51
description:
---

```
新建的文章文件就包含上面的内容：
+ title:文章标题，默认为设置的文章链接，可以修改为其他文字，可以为中文
+ tags:文章标签，可以参考标签页已有的进行设置，也可以新建自己的。如果不想设置请直接删除这一配置项
+ cover:文章封面图。文章封面图片统一保存于`hexo/source/img/`内
+ categories:文章分类，设置方法类似tag
+ data:文件新建时间，自动生成。主页文章排序依靠时间，修改为较大的值可用于置顶文章，但是一般不建议设置置顶
+ description:简介描述。随便写两句话介绍一下就好。建议在此处加入文章作者信息(如果不是Triority本人编辑的话)

编辑完成应该类似这样，以本篇文章为例：
```md
---
title: 博客文章编辑发布指南
tags:
  - hexo
  - 文档
cover: /img/RUN.png
categories:
  - 文档&笔记
date: 2024-07-22 18:33:41
description: 博客帮助文件
---
```

{% note danger modern %}
不需要的配置项记得删除，比如你不想写description就把这一行全都删掉，否则文件生成会报错。
如果你添加了新的categories，请编辑模板文件加上你新增的分类字符串，模板文件位于`/hexo/scaffolds/post.md`
{% endnote %}

# 内容编辑
## markdown
markdown语言语法请自行学习，初期使用不熟练推荐使用开源项目：[Editor.md](https://pandao.github.io/editor.md/)
## 资源文件路径
新建文章时，除了文章的文本文件``/hexo/source/[year]/[name].md``同时还会新建`/hexo/source/[year]/[name]`文件夹，对于在文章中使用的文件，均应保存在此处，包括图片，文件等内容。调用时直接使用文件名即可。

例如文章中添加的图片`![](img.img)`，图片`img.img`直接保存在上述文件夹即可，文件同理

{% note danger modern %}
注意：由于服务器由阿里云提供，存储设备为机械硬盘，如果在这部分放了过多(>5)大文件(>5MB)，可能在资源生成阶段导致IOPS超出限定值导致服务器阻塞死机，务必注意。
{% endnote %}

## 标签外挂等特殊语法
这里只说一些常用的，因为标签外挂语法太多了，参见[文档](https://butterfly.js.org/posts/2df239ce/)
### 插入图片
```
//使用插件的语法
{% asset_img xxx.png 描述 %}
//Markdown语法
![描述](xxx.png)
```

### 插入视频
```
{% dplayer "url=wwww.xxx.cn/xxx.mp4" %}
{% dplayer "url=/video/xxx.mp4" %}
```

### 站内跳转
虽然可以直接使用markdown超链接直接跳转，但是不建议这样做。因为一旦更改了域名所有文章内的链接都将失效，因此建议使用`post_link`标签。

```
{% post_link filename [title] [escape] %}
```

这样就会跳转到文件名为`filename.md`的文章，并显示标题为`[title]`。

{% post_path `CQWWRTTY2024` 'RTTY竞赛' %}

也可以跳转到某个特定章节：`post_link`标签后加上`#`和章节标题
```
{% post_path `CQWWRTTY2024` 'RTTY' %}#BI1HT
```

{% post_path `CQWWRTTY2024` 'RTTY竞赛BI1HT' %}#BI1HT

### 文件下载链接
```
[文字](xxx.zip)
```
### 哔哩哔哩视频
需要替换的内容：`src`
```
{% raw %}
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
<iframe src="//player.bilibili.com/player.html?aid=727587109&bvid=BV1LS4y1v7Nj&cid=748560556&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="position: absolute; width: 100%; height: 100%; Left: 0; top: 0;" ></iframe></div>
{% endraw %}
```
### 特殊提示
{% note danger modern %}
DANGER!!!
{% endnote %}

```
{% note danger modern %}
DANGER!!!
{% endnote %}
```


### 折叠代码

<details>
  <summary>来点击我</summary>
  于是我就被展开啦
</details>

```
<details>
  <summary>点击时的区域标题</summary>
  xxx
</details>
```

### 小黑块
这是什么？哦原来{% spoiler 这是一个小黑块 %}哦！
```
{% spoiler 被遮挡文字 %}
```


# 文件生成和git提交
文章编辑完成之后，在`/hexo`目录打开终端，输入`hexo g`进行html文件生成，如果报错请检查文章内是否有语法错误，特别是文章配置部分。

如果报错为以下内容，无需理会重新执行`hexo g`就好
```
    errno: -2,
    syscall: 'open',
    code: 'ENOENT',
    path: './search.xml'
  }
} Something's wrong. Maybe you can find the solution here: %s https://hexo.io/docs/troubleshooting.html
root@iZj6c9vpc0x2q5gkwla1erZ:/hexo#
```

然后进行git提交和推送。别忘记这一步，git已经拯救了好几次这个博客