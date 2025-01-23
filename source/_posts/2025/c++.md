---
title: C++学习笔记
cover: /img/C_grass.jpg
date: 2025-01-23 09:33:04
categories: 
- [文档&笔记]
tags:
- C++
- 笔记
---
# 主要内容
这篇文章是c++的学习笔记，仅作为我自己的备忘录使用，不包含我已经非常熟悉的内容，所以不适合入门看哦，最好有其他语言基础，当然我猜这玩意也没人看（）

# 开发环境
## windows下开发：VS studio
目前最新版本是2022，直接下载安装就能用，一切都已经准备好了

## 其他情况
一些开源开发者朋友们得知我要学一遍c++，非常热情的想要教会我，并且建议我用vscode连接wsl在ubuntu虚拟机内使用clang/msvc开发（等我先学会再说）

# 正式开始
## 基本语法

### 输入输出函数

```c++
#include <iostream>
#include <string>

struct MyStruct{
    int len;
    std::string str;
};

int main(){
    std::cout << "Hello World!\n";

    using namespace std;
    MyStruct the_string;
    cin >> the_string.str;
    the_string.len = the_string.str.length();
    cout << "The Length of "  << the_string.str << " is " << the_string.len;

    return 0;
}
```
### 指针相关操作

```c++
#include <iostream>
#include <string>

struct MyStruct {
    int len;
    std::string str;
};

int main(){
    double num = 10.0;
    //地址p为double*类型，值设置为取num的地址
    double* p = &num;
    //输出:00000004664FF714指向的值为1
    std::cout << p << ':' << *p << '\n';

    //动态数组（动态联编）和赋值
    int* pz = new int [5];
    *pz = 1;
    pz[1] = 2;
    *(pz + 2) = 3;
    std::cout << pz << ':' << pz[0] << pz[1] << pz[2] << '\n';
    //使用完成后释放（如果new有[]那么del时候要写[]，反之亦然）
    delete [] pz;

    //动态结构操作
    MyStruct* ps = new MyStruct;
    //使用->运算符访问成员
    ps->str = "str";
    //使用地址访问成员
    std::cout << (*ps).str;

    return 0;
}

```
### IO
```c++

```

