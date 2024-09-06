---
title: hexo的fluid主题设置文章首页隐藏
date: 2023-01-07 21:56:50
tags:
- hexo
description: hexo的fluidd主题设置文章首页隐藏
cover: /img/lyk2.jpg
categories: 
- 折腾记录
---
## 需求
有时候首页只想放一些关于编程的文章，日记一类不希望被放在首页上直接被看到，但是又想通过写文章记录下来。

最后实现了在文章`.md`文件开头添加`notshow`配置项，当`notshow = true`时首页不显示。
## 实现方法
在网上搜索看到这个:
[【Hexo】 设置首页隐藏指定文章](https://blog.csdn.net/m0_37323771/article/details/80672271)

这篇文章作者使用的是`next`主题，我用的是`fluid`，并没有他文章里所写的`index.swig`文件。但是在同路径下有`index.ejs`。虽然没有学过ejs但是可以看出来两个文件应该是相同的作用，即生成`index.html`文件。

作者使用的方法是for循环里添加一个if判断，我去查看了[ejs的文档](https://ejs.bootcss.com/)，其中第一个示例就是关于if：
```
<% if (user) { %>
  <h2><%= user.name %></h2>
<% } %>
```
因此，打开fluid的文件`index.ejs`，内容如下：
```
<%
if (theme.index.slogan.enable) {
  page.subtitle = theme.index.slogan.text || config.subtitle || ''
}
page.banner_img = theme.index.banner_img
page.banner_img_height = theme.index.banner_img_height
page.banner_mask_alpha = theme.index.banner_mask_alpha
%>

<% page.posts.each(function (post) { %>
  <div class="row mx-auto index-card">
    <% var post_url = url_for(post.path), cover = post.cover || theme.post.default_cover %>
    <% if(cover) { %>
      <div class="col-12 col-md-4 m-auto index-img">
        <a href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
          <img src="<%= url_for(cover) %>" alt="<%= post.title %>">
        </a>
      </div>
    <% } %>
    <article class="col-12 col-md-<%= cover ? '8' : '12' %> mx-auto index-info">
      <h1 class="index-header">
        <% if (theme.index.post_sticky && theme.index.post_sticky.enable && post.sticky > 0) { %>
          <i class="index-pin <%= theme.index.post_sticky && theme.index.post_sticky.icon %>" title="Pin on top"></i>
        <% } %>
        <a href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
          <%= post.title %>
        </a>
      </h1>

      <a class="index-excerpt" href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
        <div>
          <% var excerpt = post.description || post.excerpt || (theme.index.auto_excerpt.enable && post.content) %>
          <%- escape_html(strip_html(excerpt).substring(0, 200).trim()).replace(/\n/g, ' ') %>
        </div>
      </a>

      <div class="index-btm post-metas">
        <% if(theme.index.post_meta.date ) { %>
          <div class="post-meta mr-3">
            <i class="iconfont icon-date"></i>
            <time datetime="<%= full_date(post.date, 'YYYY-MM-DD HH:mm') %>" pubdate>
              <%- date(post.date, config.date_format) %>
            </time>
          </div>
        <% } %>
        <% if(theme.index.post_meta.category && post.categories.length > 0) { %>
          <div class="post-meta mr-3 d-flex align-items-center">
            <i class="iconfont icon-category"></i>
            <%- partial('_partials/category-chains', { categories: post.categories, limit: 1 }) %>
          </div>
        <% } %>
        <% if(theme.index.post_meta.tag && post.tags.length > 0) { %>
          <div class="post-meta">
            <i class="iconfont icon-tags"></i>
            <% post.tags.each(function(tag){ %>
              <a href="<%= url_for(tag.path) %>">#<%- tag.name %></a>
            <% }) %>
          </div>
        <% } %>
      </div>
    </article>
  </div>
<% }) %>

<%- partial('_partials/paginator') %>
```
猜测从这里开始进入每篇文章的循环：
```
<% page.posts.each(function (post) { %>
```
因此把
```
<% if(post.notshow != true) { %>
```
放在下面，如果在文章开头写了`notshow = true`，那么文章将不会被加入到首页文章列表。

最后在下面补上大括号结束
```
<% } %>
```
## 修改后文件
```
<%
if (theme.index.slogan.enable) {
  page.subtitle = theme.index.slogan.text || config.subtitle || ''
}
page.banner_img = theme.index.banner_img
page.banner_img_height = theme.index.banner_img_height
page.banner_mask_alpha = theme.index.banner_mask_alpha
%>

<% page.posts.each(function (post) { %>
  <% if(post.notshow != true) { %>
  <div class="row mx-auto index-card">
    <% var post_url = url_for(post.path), cover = post.cover || theme.post.default_cover %>
    <% if(cover) { %>
      <div class="col-12 col-md-4 m-auto index-img">
        <a href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
          <img src="<%= url_for(cover) %>" alt="<%= post.title %>">
        </a>
      </div>
    <% } %>
    <article class="col-12 col-md-<%= cover ? '8' : '12' %> mx-auto index-info">
      <h1 class="index-header">
        <% if (theme.index.post_sticky && theme.index.post_sticky.enable && post.sticky > 0) { %>
          <i class="index-pin <%= theme.index.post_sticky && theme.index.post_sticky.icon %>" title="Pin on top"></i>
        <% } %>
        <a href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
          <%= post.title %>
        </a>
      </h1>

      <a class="index-excerpt" href="<%= post_url %>" target="<%- theme.index.post_url_target %>">
        <div>
          <% var excerpt = post.description || post.excerpt || (theme.index.auto_excerpt.enable && post.content) %>
          <%- escape_html(strip_html(excerpt).substring(0, 200).trim()).replace(/\n/g, ' ') %>
        </div>
      </a>

      <div class="index-btm post-metas">
        <% if(theme.index.post_meta.date ) { %>
          <div class="post-meta mr-3">
            <i class="iconfont icon-date"></i>
            <time datetime="<%= full_date(post.date, 'YYYY-MM-DD HH:mm') %>" pubdate>
              <%- date(post.date, config.date_format) %>
            </time>
          </div>
        <% } %>
        <% if(theme.index.post_meta.category && post.categories.length > 0) { %>
          <div class="post-meta mr-3 d-flex align-items-center">
            <i class="iconfont icon-category"></i>
            <%- partial('_partials/category-chains', { categories: post.categories, limit: 1 }) %>
          </div>
        <% } %>
        <% if(theme.index.post_meta.tag && post.tags.length > 0) { %>
          <div class="post-meta">
            <i class="iconfont icon-tags"></i>
            <% post.tags.each(function(tag){ %>
              <a href="<%= url_for(tag.path) %>">#<%- tag.name %></a>
            <% }) %>
          </div>
        <% } %>
      </div>
    </article>
  </div>
  <% } %>
<% }) %>

<%- partial('_partials/paginator') %>

```