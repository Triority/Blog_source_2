---
title: pytorch模型版本修改
tags:
  - 神经网络
date: 2023-07-25 17:59:34
categories:
- 折腾记录
---
在torch1.6版本及其以后，torch.save函数使用了一种新的文件格式。torch.load任然保持着对旧版本的兼容，如果高版本环境下想要保存低版本兼容的模型文件格式，可以使用_use_new_zipfile_serialization=False参数设定
```
The 1.6 release of PyTorch switched torch.save to use a new zipfile-based file format. 
torch.load still retains the ability to load files in the old format. 
If for any reason you want torch.save to use the old format, 
pass the kwarg _use_new_zipfile_serialization=False.
```
但是如果低版本使用高版本模型文件就会报错，因此写了一个转换程序批量转换所有模型文件。

程序也在我的photo_data_maker仓库里，方便训练完直接调用

```
import torch
import os

models_old_path = 'models_old'
models_new_path = 'models_new'

for i in os.listdir(models_old_path):
    state_dict = torch.load(os.path.join(models_old_path, i), map_location="cpu")
    torch.save(state_dict, os.path.join(models_new_path, i), _use_new_zipfile_serialization=False)
    print(i, 'saved')
```