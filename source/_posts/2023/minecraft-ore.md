---
title: minecraft矿石生成概率机制
tags:
  - minecraft
cover: /img/Ore_Layout.webp
categories:
- 整活&游戏
notshow: false
date: 2023-04-04 6:54:12
description: minecraft矿石生成概率机制
---
## 主世界
### 概率测算
![生成概率图](1.18_ore_distribution.webp)

![统计表](QQ截图20230404170706.png)

![扫描统计图](OreDistribution_1-18-1_Simplified.webp)

> 此图片展示的是Java版1.18.1中主世界矿石的逐层分布情况，通过扫描515212个区块得到。
> 图1展示的是在被扫描的区块中，矿石方块的绝对数量。矿脉中的粗铜块和粗铁块按其9倍数量计入对应的矿石块中。
> 图2展示的是用对数标度表示的图1的数据。这样是为了使不同矿石的图象（尤其是绿宝石矿石）更明显。
> 图3展示的是矿石在各高度上的相对比例。空气方块、水以及“装饰性”方块（例如楼梯、炼药锅、树叶等）不列入计算。各高度上矿石方块的相对比例可以解释为在矿石生成过程中，固体方块被成功替换成矿石方块的概率。
> 当然，由于海平面以上较高高度处固体方块出现的频率要更少，以上统计数据在这些高度上会不太可靠

### 矿工策略

Y轴策略：
+ `-50`：红石，钻石，金
+ `20`：铜，铁，煤


## 下界
### 概率测算
![扫描统计图](Ancient_Debris_Spawn_Rate_Per_Layer.webp)

![统计表](QQ截图20230404170559.png)

### 矿工策略
emmm只要你床准备的够多，根本不需要策略hhh
