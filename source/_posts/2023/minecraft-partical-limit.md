---
title: Minecraft编辑源码方式修改partical数量限制
tags:
  - minecraft
cover: /img/villager_particle.jpg
categories:
- [折腾记录]
- [整活&游戏]
notshow: false
date: 2023-01-22 13:12:32
description: 新年快乐！
---
## 修改partical数量限制
今天是大年初一。昨天晚上用replay这个mod在1.12.2的服务器里录制了一段烟花表演，但是烟花生成的粒子数量实在是过于庞大，以至于烟花刚爆炸，生成的粒子就因为达到了数量上限而小时，只剩下爆炸产生的黑色球状粒子，巨丑hhh

于是就需要解除mc的粒子数量限制。想要实现这个目标，有两种方法，一种是直接修改客户端，修改数量限制，另一种是使用mod重写原版的粒子系统。显而易见，第一种方法更合适。

## 反编译minecraft
### 关于mcp
Minecraft是闭源的，但是为了编写模组，有了人力反编译的项目，比如即将使用的`mcp`，很幸运他们更新到了1.12版本，正好就是服务器使用的。再后来mojang官方提供了对照表，也就不再需要那么麻烦了。不过应该注意传播修改过的客户端是违反mojang的用户协议的。
### mcp的下载和使用
[mcp相关信息的wiki](https://minecraft.fandom.com/zh/wiki/%E8%BE%85%E5%8A%A9%E7%A8%8B%E5%BA%8F%E4%B8%8E%E7%BC%96%E8%BE%91%E5%99%A8/Mod_Coder_Pack#%E9%93%BE%E6%8E%A5)

[1.12.2修改过的mcp下载](https://cr.triority.cc/f/VETK/mc-1.12.2-source_files-master.zip)

至于使用方法，文件里面有`docs`文件夹，里面是文档。需要注意java版本，比如mc的1.12.2需要使用java8，最开始因为是17的环境所以失败。

## 修改partical数量限制代码
反编译完成后，客户端代码位于`src\minecraft\net\minecraft\`。需要修改的文件是此目录下的`client\particle\ParticleManager.java`。这段代码在第190行：
```
if (!this.queue.isEmpty())
        {
            for (Particle particle = this.queue.poll(); particle != null; particle = this.queue.poll())
            {
                int j = particle.getFXLayer();
                int k = particle.shouldDisableDepth() ? 0 : 1;

                if (this.fxLayers[j][k].size() >= 2147483647)
                {
                    this.fxLayers[j][k].removeFirst();
                }

                this.fxLayers[j][k].add(particle);
            }
        }
```
这里我已经把上限值改为了`2147483647`，应该够了吧，乐，要是渲染这些粒子能有0.1Fps就不错了hhh

## 重新编译
### 创建项目目录
这里需要`IntelliJ IDEA`来编译。其实修改也可以在这里，只不过我要改的不多直接用`vscode`改完了。

首先新建项目：

![新建](QQ截图20230122150214.png)

然后将mcp目录下的`jars`文件夹复制到新建的项目目录。

由于idea不会读取全部子目录内的库，所以使用搜索找出`libraries`内的全部`.jar`文件，剪切出来，项目目录新建一个`lib`文件夹，粘贴进去，然后`libraries`文件夹就可以删掉了。

项目路径新建一个资源目录`resources`，将原客户端包内的`log4j.xml`,`pack.png`以及`assets`目录复制进去。

最后，将mcp反编译得到的代码`src\minecraft\`内的文件复制到项目目录`src`文件夹即可。

### 编译配置
打开`idea`的`Project Structure`项目结构。

在子目录`libraries`，新建选择`java`然后选择刚才创建的`lib`目录。

再修改子目录`Modules`，选中刚才新建的`resources`，选择上面的`Resources`将其设置为资源目录。

确认上述修改后，继续修改启动项。

创建一个启动项，选择`Application`，将`Main Class`主类设置为`Start`。

然后将工作目录`Working directory`设置为之前复制来的`jars`目录。

在`modify options`中选择`add VM options`，在其中填写`natives`目录路径，在这里就是`-Djava.library.path=versions\1.12.2\1.12.2-natives`。

此时按下`Start`按钮就可以看到mc客户端启动啦

![客户端启动](QQ截图20230122161722.png)

## 打包客户端
打开`Project Structure`项目结构，选择`Artifacts`，新建选择`Jar`内的`Empty`，修改`Output Directory`导出路径，当然不改也可以。

然后将右侧的双击移到左侧：

![双击或拖动](QQ截图20230122162554.png)

最后在`build`菜单中选择`build Artifacts`，选择`buld`，等待编译完成即可

此时就可以替换掉原来的客户端文件开始渲染啦！

![输出成功](QQ截图20230122163156.png)