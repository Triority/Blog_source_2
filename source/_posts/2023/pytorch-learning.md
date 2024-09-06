---
title: 使用pytorch设计神经网络
tags:
  - 神经网络
cover: /img/QQ截图20230920192636.png
categories:
- 文档&笔记
date: 2023-09-20 18:08:22
description: pytorch？蟒蛇火把！
---
# START
## PLAN
有一个[名不符实但是不错的教程文章](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)，首先是跟着这个教程摸索一下

主要目的还是用神经网络做图像处理，比如基础的分类，然后实验室其他同学正在做智能车5G组的比赛，我想能不能实现在树莓派上识别摄像头拍到的操场跑道线，帧率最好不低于30Fps，之后也许会在做点别的？以后再补充

## NEURAL NETWORKS
定义一个神经网络(中文注释是我自己的理解可能有错误)
```py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# 定义网络
class Net(nn.Module):

    def __init__(self):
        # 继承的父类初始化
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # 一层输入，6层输出，卷积核5x5
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        # 三个全连接层，从卷积之后的16*5*5到输出的10个类别
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        # 对输入进行之前定义的卷积，然后使用RELU激活，然后使用2*2的窗口最大池化
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square, you can specify with a single number
        # 上面的(2, 2)也可以简写为2
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        # 形状改为一维进入全连接层进行两层连接计算和激活
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()
print(net)
print('------------------------------------')

# 输入一个随机数据看看输出
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)
print('------------------------------------')

# loss计算
# 随机一个目标值
target = torch.randn(10)  # a dummy target, for example
# 修改随机生成的目标张量为输出的形状
target = target.view(1, -1)  # make it the same shape as output
# 计算loss（均方误差）
criterion = nn.MSELoss()
loss = criterion(out, target)
print(loss)
print('------------------------------------')

# 将所有参数的梯度缓冲区归零，删除积累数据,计算当前梯度
net.zero_grad()     # zeroes the gradient buffers of all parameters
print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)
loss.backward()
print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)
print('------------------------------------')

# 更新权重
# create your optimizer
# 创建优化器，使用随机梯度下降(SGD,Stochastic Gradient Descent)
optimizer = optim.SGD(net.parameters(), lr=0.01)
# in your training loop:
# 训练的循环，这里我只是随便测试，仍然使用之前的网络输入和生成的目标
for i in range(20):
    optimizer.zero_grad()   # zero the gradient buffers
    output = net(input)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()    # Does the update
# 可以看到再次计算loss以及比之前有所下降
out = net(input)
loss = criterion(out, target)
print(loss)
```
这个是我运行了一次的终端输出：
```
Net(
  (conv1): Conv2d(1, 6, kernel_size=(5, 5), stride=(1, 1))
  (conv2): Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1))
  (fc1): Linear(in_features=400, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=84, bias=True)
  (fc3): Linear(in_features=84, out_features=10, bias=True)
)
------------------------------------
tensor([[-0.0397,  0.0617, -0.0083, -0.1553, -0.0229,  0.0050, -0.0213, -0.0916,
         -0.0209,  0.1796]], grad_fn=<AddmmBackward0>)
------------------------------------
tensor(2.0191, grad_fn=<MseLossBackward0>)
------------------------------------
conv1.bias.grad before backward
None
conv1.bias.grad after backward
tensor([-0.0170,  0.0098,  0.0320,  0.0319, -0.0213, -0.0409])
------------------------------------
tensor(0.1494, grad_fn=<MseLossBackward0>)

```
## TRAINING A CLASSIFIER
### What about data?
使用CIFAR10数据集进行测试，torchvision可以自动下载
```py
import torch
import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
```
之后再使用这个数据集也就不需要再次下载了，可以把上面参数的`download=True`改成`False`就不会再提示数据集已下载了

进行一次下载之后就可以尝试加载数据集并随机显示四张图片：
```py
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms

# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)
testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# get some random training images
dataiter = iter(trainloader)
images, labels = next(dataiter)

# show images
imshow(torchvision.utils.make_grid(images))
# print labels
print(' '.join(f'{classes[labels[j]]:5s}' for j in range(batch_size)))

```

### Training an image classifier
下面的程序使用整个数据集进行了训练，并保存模型
```py
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入修改为3通道图像
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

if __name__ == '__main__':
    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    # 循环遍历数据集
    for epoch in range(2):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            # 计算输出最近2000图片的平均loss
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0

    print('Finished Training')
    # 保存模型
    PATH = './cifar_net.pth'
    torch.save(net.state_dict(), PATH)

```
### Test the network on the test data
```py
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=False, transform=transform)
# 下面的shuffle改成了True使得测试集顺序随机
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=True, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

if __name__ == '__main__':
    # 随机测试图片
    dataiter = iter(testloader)
    images, labels = next(dataiter)

    # print images
    # 显示图片和其类别
    print('GroundTruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))
    imshow(torchvision.utils.make_grid(images))

    # 加载模型
    net = Net()
    PATH = './cifar_net.pth'
    net.load_state_dict(torch.load(PATH))
    # 模型计算
    outputs = net(images)
    # 取最高置信度的输出
    _, predicted = torch.max(outputs, 1)
    print('Predicted: ', ' '.join(f'{classes[predicted[j]]:5s}' for j in range(4)))
    
```
## Training on GPU
检查是否有cuda设备
```py
import torch
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)
```
然后这样就可以迁移到GPU：
```py
net.to(device)
# you will have to send the inputs and targets at every step to the GPU too
inputs, labels = data[0].to(device), data[1].to(device)
```
将之前训练的程序改为GPU计算：
```py
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=True, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入修改为3通道图像
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

if __name__ == '__main__':
    net = Net()
    net.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    # 循环遍历数据集
    for epoch in range(2):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data[0].to(device), data[1].to(device)
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            # 计算输出最近2000图片的平均loss
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0

    print('Finished Training')
    # 保存模型
    PATH = './cifar_net.pth'
    torch.save(net.state_dict(), PATH)

```
## Where do I go next?
我真的好喜欢这个教程，特别是最后的`Where do I go next?`这部分，直接留[链接](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#where-do-i-go-next)吧
