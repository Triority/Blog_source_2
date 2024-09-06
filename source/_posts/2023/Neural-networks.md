---
title: 神经网络学习：从尝试识别手写数字开始
tags:
  - 神经网络
  - python
cover: /img/v2-777808fc5b00e7727df4dc835c1fc44f_1440w.jpg
categories:
- [文档&笔记]
- [折腾记录]
- [值得一提的文章]
notshow: false
date: 2023-04-24 04:53:00
description: 神经网络入门笔记
---
# first
文章创建时间就很离谱：`2023-04-24 04:53:00`，晚上躺在床上感觉饿了，但是懒得下床买吃的，就一直饿的睡不着，终于在三点起床了下楼吃饱喝足了，回来毫无困意，于是开始写这篇离谱的文章
# 起点：分类任务
## 任务描述
已知四个数据点(1,1)(-1,1)(-1,-1)(1,-1)，这四个点分别对应I~IV象限，如果这时候给我们一个新的坐标点(比如(2,2))，那么它应该属于哪个象限呢？(当然是第I象限，但我们的任务是要让机器知道)

“分类”是神经网络的一大应用，我们使用神经网络完成这个分类任务。
## 网络结构：理论基础
我们构建一个两层神经网络，理论上两层神经网络已经可以拟合任意函数。这个神经网络的结构如下图：
![简化网络结构](v2-7ee8cabcbd707dd4deab7155af2ba4cd_1440w.webp)
### 正向传播
#### 输入层
在我们的例子中，输入层是坐标值，例如(1,1)，这是一个包含两个元素的数组，也可以看作是一个1*2的矩阵。输入层的元素维度与输入量的特征相关，如果输入的是一张32*32的灰度图，那么输入层就是一个32*32的矩阵
#### 输入层到隐藏层
连接输入层和隐藏层的是W1和b1。由X计算得到H就是矩阵运算`H=X*W1+b1`。如上图中所示，在设定隐藏层为50维(也可以理解成50个神经元)之后，矩阵H的大小为(1*50)的矩阵
#### 隐藏层到输出层
连接隐藏层和输出层的是W2和b2。同样是通过矩阵运算`Y=X*W2+b2`
#### 激活层
通过上述两个线性方程的计算，我们就能得到最终的输出Y了，但是一系列线性方程的运算最终都可以用一个线性方程表示。也就是说，上述两个式子联立后可以用一个线性方程表达。对于两次神经网络是这样，就算网络深度加到100层，也依然是这样。这样的话神经网络就失去了意义。所以这里要对网络注入灵魂：激活层。

激活层是为矩阵运算的结果添加非线性的。常用的激活函数有三种，分别是阶跃函数、Sigmoid和ReLU。

|  ![](d000baa1cd11728b445e79fccbfcc3cec2fd2cf8.jfif) | ![](d009b3de9c82d158dfb4e7218a0a19d8bc3e426f.jfif)  |  ![](OIP-C.jfif) |
| :------------: | :------------: | :------------: |
| 阶跃函数  | Sigmoid  | ReLU  |
| 当输入小于等于0时，输出0；当输入大于0时，输出1  | 当输入趋近于正无穷/负无穷时，输出无限接近于1/0  | 当输入小于0时，输出0；当输入大于0时，输出等于输入  |

阶跃函数输出值是跳变的，且只有二值，较少使用；Sigmoid函数在当x的绝对值较大时，曲线的斜率变化很小(梯度消失)，并且计算较复杂；ReLU是当前较为常用的激活函数。
每个隐藏层计算(矩阵线性运算)之后，都需要加一层激活层，要不然该层线性计算是没有意义的。

此时网络结构以及变成了：
![](v2-0ced86f32dfa241fc9de10421edbd9b4_1440w.webp)

#### 输出的正规化
在上一步之后，输出Y的值可能会是(3,1,0.1,0.5)这样的矩阵，诚然我们可以找到里边的最大值“3”，从而找到对应的分类为I，但是这并不直观。我们想让最终的输出为概率，也就是说可以生成像(90%,5%,2%,3%)这样的结果，这样做不仅可以找到最大概率的分类，而且可以知道各个分类计算的概率值。

计算公式如下：这样求出的结果中，所有元素的和一定为1，而每个元素可以代表概率值
![](v2-3ad93ae576918ff385485dab6a2e6b87_1440w.png)

我们将使用这个计算公式做输出结果正规化处理的层叫做“Softmax”层。此时的神经网络将变成如下图所示：
![](v2-01285f87ff9d523f62d2d4f6586583c5_1440w.webp)

#### 交叉熵损失(Cross Entropy Error)
比如，Softmax输出的结果是(90%,5%,3%,2%)，真实的结果是(100%,0,0,0)。虽然输出的结果可以正确分类，但是与真实结果之间是有差距的，一个优秀的网络对结果的预测要无限接近于100%，为此，我们需要将Softmax输出结果的好坏程度做一个“量化”。常用且巧妙的方法是，求对数的负数。用90%举例，对数的负数就是：-log0.9=0.046

概率越接近100%，该计算结果值越接近于0，说明结果越准确，该输出叫做`交叉熵损失`。我们训练神经网络的目的，就是尽可能地减少这个损失。

此时的网络如下图：
![](v2-6fac69d2abab24639943ebaab0b70bde_1440w.webp)

### 反向传播
反向传播就是一个参数优化的过程，优化对象就是网络中的所有W和b。神经网络的神奇之处，就在于它可以自动做W和b的优化。使用的方法叫做梯度下降法
### 迭代
神经网络需要反复迭代。如上述例子中，第一次计算得到的概率是90%，交叉熵损失值是0.046；将该损失值反向传播，使W1,b1,W2,b2做相应微调；再做第二次运算，此时的概率可能就会提高到92%，相应地，损失值也会下降，然后再反向传播损失值，微调参数W1,b1,W2,b2。依次类推，损失值越来越小，直到我们满意为止。此时我们就得到了理想的W1,b1,W2,b2。

此时如果将任意一组坐标作为输入，利用图4或图5的流程，就能得到分类结果。
## 网络实现：使用python实现分类功能
### 前置任务
导入numpy库
```
import numpy as np
```
### 正向传播函数
#### 函数代码
```
def affine_forward(x, w, b):   
    out = None                       # 初始化返回值为None
    # 输入参数处理
    n = x.shape[0]                   # 获取输入参数X的形状
    x_row = x.reshape(n, -1)         # (N,D)
    # 矩阵的线性运算
    out = np.dot(x_row, w) + b       # (N,M)
    # 缓存值，反向传播时使用
    cache = (x, w, b)
    return out,cache
```
affine_forward函数，用于计算公式：`H=X*W1+b1`，输入参数就是公式中的矩阵X，W1和b1，对应到程序中就是x，w和b。
#### 输入参数处理
程序中的输入参数x，其形状可以是(n，d_1，...，d_k).在我们这个例子中，输入参数x是：
```
[[2,1],
[-1,1],
[-1,-1],
[1,-1]]
```
它是一个4行2列的二维数组，那么x的形状就是(4,2)，对应的参数n=4，d_1=2。这是我们用来做训练的坐标数据，分别对应了I、II、III、IV象限。

在某些应用场景中，x的维度可能更高。比如对于一个20*20像素的4张灰度图，x的形状将是(4,20,20)，对应的参数就是n=4，d_1=20，d_2=20。n代表的是同时用于计算前向传播的数据有几组，后边的参数d_1~d_k代表的是数据本身的形状。

为了方便计算，对于这种维度大于2的x来说，需要对其进行重新塑形，也就是将(4,20,20)的高维数组变化为(4,20*20)这样的二位数组。
这样变换之后高维的向量被“拍扁”成一维向量(长度为20*20的一维向量)，对应的W和b也都是一维的，既统一了参数形式，又不会影响数据的正常使用。

`x.reshape(n,-1)`是对x重新塑形，即保留第0维，其他维度排列成1维。

#### 矩阵的线性运算
`.dot`就是numpy中的函数，可以实现x_row与w的矩阵相乘。x_row的形状为(N,D)，w的形状为(D,M)，得到的out的形状是(N,M)

### 反向传播函数
```
def affine_backward(dout, cache): 
  # 读取缓存
  x, w, b = cache
  # 返回值初始化
  dx, dw, db = None, None, None
  # 仿射变换反向传播：更新参数w的值-计算流向下一个节点的数值-更新参数b的值
  dx = np.dot(dout, w.T)                       # (N,D)    
  dx = np.reshape(dx, x.shape)                 # (N,d1,...,d_k)   
  x_row = x.reshape(x.shape[0], -1)            # (N,D)    
  dw = np.dot(x_row.T, dout)                   # (D,M)    
  db = np.sum(dout, axis=0, keepdims=True)     # (1,M)    
  return dx, dw, db
```
### 学习参数初始化
```
# 用于训练的坐标，对应的是I、II、III、IV象限
X = np.array([[2,1], [-1,1], [-1,-1], [1,-1]])
# 标签，对应的是I、II、III、IV象限
t = np.array([0,1,2,3])
# 生成随机数保持一致
np.random.seed(1)

# 输入参数的维度，此处为2，即每个坐标用两个数表示
input_dim = X.shape[1]
# 输出参数的维度，此处为4，即最终分为四个象限
num_classes = t.shape[0]
# 隐藏层维度，可调参数
hidden_dim = 50
# 正则化强度，可调参数
reg = 0.001
# 梯度下降的学习率，为可调参数
epsilon = 0.001
# 初始化W1，W2，b1，b2
W1 = np.random.randn(input_dim, hidden_dim) # 生成随机矩阵
W2 = np.random.randn(hidden_dim, num_classes)
b1 = np.zeros((1, hidden_dim))  # 生成以0填充的矩阵
b2 = np.zeros((1, num_classes))
```
对一些必要的参数进行了初始化。对于训练数据以及训练模型已经确定的网络来说，为了得到更好的训练效果需要调节的参数就是上述的隐藏层维度、正则化强度和梯度下降的学习率，以及下一节中的训练循环次数。

### 训练与迭代
```
#训练的循环次数为10000
for j in range(10000):

  # 前向传播
  # 第一层前向传播。调用了之前写的前向传播的函数，完成了第一层网络的矩阵线性代数运算
  H,fc_cache = affine_forward(X,W1,b1)
  # 激活函数。从0和H中选择较大的值赋给H，也就是实现了ReLU激活层函数。
  H = np.maximum(0, H)
  # 缓存第一层激活后的结果
  relu_cache = H
  # 第二层网络的矩阵线性代数运算
  Y,cachey = affine_forward(H,W2,b2)     

  # 输出的正规化：Softmax层计算。之前我们说过的Softmax的计算公式在实际应用中会存在一个问题，比如i的值等于1000时，e^1000在计算机中会变成无穷大的inf，后续计算将无法完成，所以程序中会对计算公式做一些修改。修改见下文说明。
  probs = np.exp(Y - np.max(Y, axis=1, keepdims=True))    
  probs /= np.sum(probs, axis=1, keepdims=True)

  # 计算loss值
  # 取了最终输出的维度，这个例子中为4，即四个象限
  N = Y.shape[0]
  # 打印各个数据的正确解标签对应的神经网络的输出
  print(probs[np.arange(N), t])
  # 先求了N维数据中的交叉熵损失，然后对这N个交叉熵损失求平均值，作为最终loss值
  loss = -np.sum(np.log(probs[np.arange(N), t])) / N
  print(loss)

  # 反向传播
  # 以Softmax输出结果作为反向输出的起点
  dx = probs.copy()
  # 将Softmax的输出值赋给dx， 这里dx代表反向传播的主线值
  dx[np.arange(N), t] -= 1
  # 反向传播到softmax前
  dx /= N
  # 反向传播至第二层前
  dh1, dW2, db2 = affine_backward(dx, cachey)
  # 反向传播至激活层前
  dh1[relu_cache <= 0] = 0
  # 反向传播至第一层前
  dX, dW1, db1 = affine_backward(dh1, fc_cache)

  # 参数更新
  # 引入正则化惩罚项更新dW
  dW2 += reg * W2
  dW1 += reg * W1
  # 引入学习率更新W和b
  W2 += -epsilon * dW2
  b2 += -epsilon * db2
  W1 += -epsilon * dW1
  b1 += -epsilon * db1
```
修改说明：
原公式为![](v2-3ad93ae576918ff385485dab6a2e6b87_1440w.png)
在指数上减去常数C不影响最终结果，而这个常数C通常取i中的最大值。
![](v2-7e7f127681085bfd26ae59511ab2c8fd_1440w.png)
第一句probs = np.exp(Y - np.max(Y, axis=1, keepdims=True)) 就是求输出各个行的指数值，举个例子，Y的值如果是：
```
[[-4,17,20,-4],
[10,-2,5,3],
[-5,3,4,10],
[-5,5,5,2]]
```
np.max(Y, axis=1, keepdims=True)计算得到的是`[[20],[10],[10],[5]]`，后边括号里的参数axis代表以竖轴为基准 ，在同行中取值； keepdims=True代表保持矩阵的二维特性。
所以`np.exp(Y - np.max(Y, axis=1, keepdims=True))`代表：Y矩阵中每个值减掉改行最大值后再取对数。

### 验证
```
test = np.array([[2,2],[-2,2],[-2,-2],[2,-2]])
#仿射
H,fc_cache = affine_forward(test,W1,b1)
# 激活
H = np.maximum(0, H)
relu_cache = H
# 仿射
Y,cachey = affine_forward(H,W2,b2)
# Softmax
probs = np.exp(Y - np.max(Y, axis=1, keepdims=True))    
probs /= np.sum(probs, axis=1, keepdims=True)  # Softmax
print(probs)
for k in range(4):
  print(test[k,:],"所在的象限为",np.argmax(probs[k,:])+1)
```
其实验证的方法和训练时的正向传播的过程基本一致，即第一层网络线性计算→激活→第二层网络线性计算→Softmax→得到分类结果.
### 源码
```
import numpy as np


# 前向传播函数
# - x：包含输入数据的numpy数组，形状为(N，d_1，...，d_k)
# - w：形状为(D，M)的一系列权重
# - b：偏置，形状为(M，)
def affine_forward(x, w, b):
    out = None  # 初始化返回值为None
    N = x.shape[0]  # 重置输入参数X的形状
    x_row = x.reshape(N, -1)  # (N,D)
    out = np.dot(x_row, w) + b  # (N,M)
    cache = (x, w, b)  # 缓存值，反向传播时使用
    return out, cache


# 反向传播函数
# - x：包含输入数据的numpy数组，形状为(N，d_1，...，d_k)
# - w：形状(D，M)的一系列权重
# - b：偏置，形状为(M，)
def affine_backward(dout, cache):
    x, w, b = cache  # 读取缓存
    dx, dw, db = None, None, None  # 返回值初始化
    dx = np.dot(dout, w.T)  # (N,D)
    dx = np.reshape(dx, x.shape)  # (N,d1,...,d_k)
    x_row = x.reshape(x.shape[0], -1)  # (N,D)
    dw = np.dot(x_row.T, dout)  # (D,M)
    db = np.sum(dout, axis=0, keepdims=True)  # (1,M)
    return dx, dw, db


X = np.array([[2, 1],
              [-1, 1],
              [-1, -1],
              [1, -1]])  # 用于训练的坐标，对应的是I、II、III、IV象限
t = np.array([0, 1, 2, 3])  # 标签，对应的是I、II、III、IV象限
# np.random.seed(1)  # 有这行语句，你们生成的随机数就和我一样了

# 一些初始化参数
input_dim = X.shape[1]  # 输入参数的维度，此处为2，即每个坐标用两个数表示
num_classes = t.shape[0]  # 输出参数的维度，此处为4，即最终分为四个象限
hidden_dim = 50  # 隐藏层维度，为可调参数
reg = 0.001  # 正则化强度，为可调参数
epsilon = 0.001  # 梯度下降的学习率，为可调参数
# 初始化W1，W2，b1，b2
W1 = np.random.randn(input_dim, hidden_dim)  # (2,50)
W2 = np.random.randn(hidden_dim, num_classes)  # (50,4)
b1 = np.zeros((1, hidden_dim))  # (1,50)
b2 = np.zeros((1, num_classes))  # (1,4)

for j in range(10000):  # 这里设置了训练的循环次数为10000
    # ①前向传播
    H, fc_cache = affine_forward(X, W1, b1)  # 第一层前向传播
    H = np.maximum(0, H)  # 激活
    relu_cache = H  # 缓存第一层激活后的结果
    Y, cachey = affine_forward(H, W2, b2)  # 第二层前向传播
    # ②Softmax层计算
    probs = np.exp(Y - np.max(Y, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)  # Softmax算法实现
    # ③计算loss值
    N = Y.shape[0]  # 值为4
    print(probs[np.arange(N), t])  # 打印各个数据的正确解标签对应的神经网络的输出
    loss = -np.sum(np.log(probs[np.arange(N), t])) / N  # 计算loss
    print(loss)  # 打印loss
    # ④反向传播
    dx = probs.copy()  # 以Softmax输出结果作为反向输出的起点
    dx[np.arange(N), t] -= 1  #
    dx /= N  # 到这里是反向传播到softmax前
    dh1, dW2, db2 = affine_backward(dx, cachey)  # 反向传播至第二层前
    dh1[relu_cache <= 0] = 0  # 反向传播至激活层前
    dX, dW1, db1 = affine_backward(dh1, fc_cache)  # 反向传播至第一层前
    # ⑤参数更新
    dW2 += reg * W2
    dW1 += reg * W1
    W2 += -epsilon * dW2
    b2 += -epsilon * db2
    W1 += -epsilon * dW1
    b1 += -epsilon * db1

test = np.array([[2, 2], [-2, 2], [-2, -2], [2, -1]])
H, fc_cache = affine_forward(test, W1, b1)  # 仿射
H = np.maximum(0, H)  # 激活
relu_cache = H
Y, cachey = affine_forward(H, W2, b2)  # 仿射
# Softmax
probs = np.exp(Y - np.max(Y, axis=1, keepdims=True))
probs /= np.sum(probs, axis=1, keepdims=True)  # Softmax
print(probs)
for k in range(4):
    print(test[k, :], "所在的象限为", np.argmax(probs[k, :]) + 1)

```
## 手写数字识别
### 数据集
#### 数据集格式
每个文件有 784 个灰度值(每行 28 个，28 列)，最后一个值是预期的输出值(实际数字)
[文本数据集](https://www.kaggle.com/datasets/jcprogjava/kaggle-digit-recognition-dataset-reformatted?resource=download)
#### 数据集解析
这个程序可以用来对文本文件做图片的可视化
```
import numpy as np
import cv2
txt_path = r'C:\Users\Triority\Desktop\kaggle data\00001.txt'
f = open(txt_path)
data_lists = f.readlines()
dataset = []
for data in data_lists:
    if len(data) == 1:
        print('数字：'+data[0])
        break
    data1 = data.strip('\n')
    data2 = data1.split('\t')
    data3 = []
    for i in range(len(data2)):
        if data2[i]=='':
            break
        data3.append(int(data2[i]))
    dataset.append(data3)
dataset = np.array(dataset, dtype=np.uint8)
cv2.imshow('name', dataset)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
```
# 使用pytorch
该说不说，前面写的都是原理解释，实际上写的很麻烦(而且很屎)，而使用pytorch可以极大简化细节。

pytorch的安装就不说了，不过可以安装使用cuda的版本加速计算。这个具体安装方法可以参考之前的文章：[pytorch环境配置及使用nanodet进行模型训练和识别](https://triority.cn/2022/nanodet-train/)。当然没有nvidia显卡的设备就没那么多麻烦了。


# 参考资料
https://zhuanlan.zhihu.com/p/65472471
https://zhuanlan.zhihu.com/p/67682601
https://zhuanlan.zhihu.com/p/66534632