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

所有示例程序都是我自己重新写的简化举例可放心参考。

# 开发环境
## windows下开发：VS studio
目前最新版本是2022，直接下载安装就能用，一切都已经准备好了

## 其他情况
一些开源开发者朋友们得知我要学一遍c++，非常热情的想要教会我，并且建议我用vscode连接wsl在ubuntu虚拟机内使用clang/msvc开发（等我先学会再说）

# 基本语法
## 数据类型长度和范围
c++标准没用固定值的规定，但是有最小标准：
+ `short`至少16位（-32,768 - 32,767）
+ `int`至少于`short`一样长
+ `long`至少32位（-2,147,483,648 - 2,147,483,647），且至少于`int`一样长
+ `long long`至少64位（-9,223,372,036,854,775,808 - 9,223,372,036,854,775,807），且至少于`long`一样长（有的系统不支持）

可以通过`#include <climits>`获取具体范围：
```c++
.
#include <iostream>
#include <climits>

int main(){
    using namespace std;
    int n_int = INT_MAX;
    short n_short = SHRT_MAX;
    long n_long = LONG_MAX;
    long long n_llong = LLONG_MAX;

    cout << "int is " << sizeof(int) << " bytes, maximum value: " << n_int << endl;
    cout << "short is " << sizeof(int) << " bytes, maximum value: " << n_short << endl;
    cout << "long is " << sizeof(int) << " bytes, maximum value: " << n_long << endl;
    cout << "long long is " << sizeof(int) << " bytes, maximum value: " << n_llong << endl;
    return 0;
}

```
在我的64位windwos系统上结果为：
```
int is 4 bytes, maximum value: 2147483647
short is 4 bytes, maximum value: 32767
long is 4 bytes, maximum value: 2147483647
long long is 4 bytes, maximum value: 9223372036854775807
```

## 输入输出函数

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
## 指针相关操作

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
    std::cout << p << ':' << *p << endl;

    //动态数组（动态联编）和赋值
    int* pz = new int [5];
    *pz = 1;
    pz[1] = 2;
    *(pz + 2) = 3;
    std::cout << pz << ':' << pz[0] << pz[1] << pz[2] << endl;
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
## 简单IO
```c++
#include <iostream>
#include <fstream>
#include <string>

int main(){
    using namespace std;

    //写入ofstream（覆盖原内容）
    ofstream outfile;
    outfile.open("info.txt");
    string str0;
    getline(cin,str0);
    outfile << str0;
    outfile.close();

    //读取ifstream
    ifstream infile;
    infile.open("info.txt");
    if (!infile.is_open()) {
        cout << "ERROR";
        exit(EXIT_FAILURE);
    }
    string str1;
    while (infile.good()){
        getline(infile,str1);
        cout << str1 << endl;
    }
    return 0;
}
```
## 函数应用
### 内联函数
函数前加`inline`，编译器将函数代码替换函数调用，减少跳转导致的时间消耗
```c++
#include <iostream>

inline long long square(long long x) {
    return x * x;
}

int main(){
    using namespace std;
    long long num;
    cin >> num;
    cout << square(num);
    return 0;
}
```
### 函数引用变量
使用引用变量作为函数参数，函数将使用原始数据而不是其副本，可用于函数处理大型结构或进行类的设计
```c++
#include <iostream>

int main(){
    using namespace std;
    int num = 100;
    int & number = num;
    cout << num << "---" << number << endl;
    number++;
    cout << num << "---" << number << endl;
    return 0;
}
```
此外需要注意，引用变量必须在创建时初始化，而且无法修改关联的变量。

使用结构引用参数只需在声明结构参数时使用引用运算符`&`即可。例如如下结构定义，函数原型应该这样编写，从而在函数中将指向该结构的引用作为参数：
```c++
struct STRUCT{
    std:string name;
    int num;
}
void FUNC(STRUCT & s);
//如果不希望函数修改传入的结构可使用const
void FUNC(const STRUCT & s);
```

### 参数重载
可以通过函数重载来设计一系列函数，他们名称相同，完成相同的操作，但是使用不同的参数列表（他们的返回值类型也可以不一样）。

### 函数模板
可以使用泛型来定义函数，避免了对函数多次几乎相同的编写
```c++
#include <iostream>

template <typename T>
void Swap(T &a, T &b);

template <typename T>
void Swap(T &a, T &b) {
    T temp;
    temp = a;
    a = b;
    b = temp;
}

int main(){
    using namespace std;
    int a = 10;
    int b = 20;
    cout << "a , b = " << a << " , " << b << endl;
    Swap(a, b);
    cout << "a , b = " << a << " , " << b << endl;

    double c = 11.4;
    double d = 51.4;
    cout << "c , d = " << c << " , " << d << endl;
    Swap(c, d);
    cout << "c , d = " << c << " , " << d << endl;
    return 0;
}

```

## 多文件编程
### 头文件
头文件应该包含以下内容：
+ 函数原型
+ 使用`#define`或`const`定义的符号常量
+ 结构声明
+ 类声明
+ 模板声明
+ 内联函数

在包含头文件时，应使用`a.h`而不是`<a.h>`，后者编译器会在存储标准头文件的位置查找，而前者先在当前工作目录查找，如果没用找到再去标准位置。

为了避免包含同一个头文件多次（可能包含了另一个包含某个头文件的头文件），可以使用
```c++
#ifndef STH
#define STH
#endif
```

### 存储持续性
+ 自动存储：函数中定义将在函数结束后释放。
+ 静态存储：在函数外定义的变量和用关键字`static`定义的变量。在整个程序运行过程中存在。
  + 链接性为外部，可在其他文件访问，必须在代码块外声明。在一个文件中定义，其他文件使用`extern`关键字声明。
  + 链接性为内部，只能在当前文件访问，必须在代码块外声明并使用`static`限定符
  + 无链接性，只能在当前函数或代码块内访问，必须在代码块内声明并使用`static`限定符
+ 线程存储：使用关键字`thread_local`声明，其生命周期和其所属线程一样长
+ 动态存储：使用`new`关键字分配，一直存在直到使用`delete`将其释放或程序结束。也被称为自由存储（free store）或堆（heap）

### 说明符和限定符
存储说明符：
+ auto（c++11中不再是说明符）
+ register
+ static
+ extern
+ thread_local（c++11新增的）
+ mutable

限定符：
+ const
+ volatile（避免编译器进行将数据复制到寄存器的优化，因为硬件等可能对其进行修改，例如串口信息）
+ mutable（用于指出即使结构或类为const，其某个成员也可以进行修改）

```c++
struct data{
    char name[10];
    mutable int accesses;
}
const data veep = {"a", 0};
strcpy(veep.name, "abc");//not allowed
veep.accesses++;//allowed
```
### 名称空间
两个名称空间的相同名称将不会导致冲突。

## 多文件编译
### 简要介绍和安装
```
完成C++项目的执行过程， 主要是分为四步: 预处理、编译、汇编、链接。g++命令确实可以对一个C++项目通过上面四步转成可执行文件，但在中大型项目里面，这样还是太复杂。 于是乎就有了MakeFile。
Makefile 文件描述了 Linux 系统下 C/C++ 工程的编译规则，它用来自动化编译 C/C++ 项目。一旦写编写好 Makefile 文件，只需要一个 make 命令，整个工程就开始自动编译，不再需要手动执行 GCC 命令。
CMake是简化MakeFile编写，可以自动生成MakeFile文件
CMake是一个跨平台的编译(Build)工具，可以用简单的语句来描述所有平台的编译过程，其是在make基础上发展而来的，早期的make需要程序员写Makefile文件，进行编译，而现在CMake能够通过对cmakelists.txt的编辑，轻松实现对复杂工程的组织

cmake编译流程：
1. 编写Cmake配置文件CMakeLists.txt, 理解成Cmake所要处理的代码
2. 执行命令 cmake path生成MakeFile, path是CmakeList.txt所在目录
3. 使用make命令进行编译
```
安装cmake并查看版本：
```
sudo apt-get install cmake
cmake --version
```
### 目录组织
+ 项目根目录下建立`build`文件夹并建立`CMakeLists.txt`文件（和.cpp和.h在一起，这里只是最简单的演示文件）
    ```
    cmake_minimum_required(VERSION 3.28)

    # set the project name
    project(main)

    # add the executable
    add_executable(main 1.cpp main.cpp)
    ```
+ build文件夹内使用cmake生成makefile
    ```
    cmake ../.
    ```
+ 编译项目
    ```
    make
    ```
+ 执行程序
    ```
    ./main
    ```
![](微信截图_20250126175713.png)

#### CMakeLists.txt
这里面的大部分命令都是固定语法，相当于我们只需要指定一些参数即可。 先整理上面几个命令，如果有其他命令需要用到，可以[去官网查看具体使用](https://cmake.org/cmake/help/v2.8.8/cmake.html#section_Commands)（当然这个页面我觉得不会有人愿意看）

+ cmake_minimum_required命令
  + `cmake_minimum_required(VERSION major[.minor[.patch[.tweak]]][FATAL_ERROR])`
  + 用于指定需要的CMake 的最低版本
  + 示例：`cmake_minimum_required(VERSION 3.28)`
+ project命令
  + `project( [languageName1 languageName2 … ] )`
  + 用于指定项目的名称，一般和项目的文件名称对应
  + 示例：`project(main)`
+ add_executable命令
  + `add_executable( [WIN32] [MACOSX_BUNDLE][EXCLUDE_FROM_ALL] source1 source2 … sourceN)`
  + 用于指定从一组源文件 source1 source2 … sourceN 编译出一个可执行文件且命名为name
  + 示例：`add_executable(main 1.cpp main.cpp)`
+ include_directories命令
  + `include_directories([AFTER|BEFORE] [SYSTEM] dir1 dir2 …)`
  + 用于设定目录，这些设定的目录将被编译器用来查找 include 文件

