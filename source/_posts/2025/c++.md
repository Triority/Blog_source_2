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
一些开源开发者朋友们得知我要学一遍c++，非常热情的想要教会我，并且建议我用vscode连接wsl在ubuntu虚拟机内使用clang/msvc开发

# 基本语法
## 数据类型长度和范围
c++标准没用固定值的规定，但是有最小标准：
+ `short`至少16位（-32,768 - 32,767）
+ `int`至少于`short`一样长
+ `long`至少32位（-2,147,483,648 - 2,147,483,647），且至少于`int`一样长
+ `long long`至少64位（-9,223,372,036,854,775,808 - 9,223,372,036,854,775,807），且至少于`long`一样长（有的系统不支持）

可以通过`#include <climits>`获取具体范围：
```c++
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
两个名称空间的相同名称将不会导致冲突。下面的代码使用新的关键字`namespace`创建了一个新的名称空间：
```c++
namespace Triority{
    int sth;
    void func();
}
```
名称空间可以是全局的也可以位于其他名称空间中，但是不能在代码块中。默认情况下其链接性为外部的（除非引用了常量）


标记一下，这一段我没写完，我要先去写cmake


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

#### vscode自动生成CMakeLists.txt
利用vscode中的cmaketools插件，可以自动生成cmakelist文件，例如需要include两个头文件生成就是这样：
```
cmake_minimum_required(VERSION 3.5.0)
project(main VERSION 0.1.0 LANGUAGES C CXX)

add_executable(main 1.cpp 2.cpp main.cpp)

```
在vscode安装`cmake`,`CMake Tools`,`Makefile Tools`三个插件，`Ctrl+shift+p`调出VSCode的指令面板，输入`cmake`，找到`cmake:quick start`，按照提示填写一个项目的名称，选择C++orC，选择构建库或者可执行文件，我这里只需要一个可执行文件，然后就会自动帮你生成一个CMakeLists


## OOP：面向对象
### 类的定义和使用
`a_class.h`:
```c++
#include <string>

class Stock{
private://默认就是private，也可以不写这个关键字
    std::string company;
    long shares;
    double share_val;
    double total_val;
    void set(){
        total_val = shares * share_val;
    }
public:
    //构造函数用于初始化
    Stock(const std::string & co, long n = 0, double pr = 0.0);
    //成员函数
    void buy(long num, double price);
    //const成员函数，保证函数不会修改调用对象
    void show() const;
    //析构函数,一般不应显式调用，如果没用定义将隐式生成，用于完成清理工作，例如进行delate内存释放
    ~Stock();
};
```
`a_class.cpp`:
```c++
#include <iostream>
#include "a_class.h"

void Stock::buy(long num, double price){
    shares += num;
    share_val = price;
    set();
}

void Stock::show() const {
    std::cout << "Company:" << company << std::endl 
        << "Shares:" << shares << std::endl
        << "Share Price:" << share_val << std::endl 
        << "Total Worth:" << total_val << std::endl;
}

Stock::Stock(const std::string & co, long n, double pr){
    company = co;
    shares = n;
    share_val = pr;
    set();
}

Stock::~Stock(){
    std::cout << "DEL " << company << std::endl;
}
```
`main.cpp`
```c++
#include <iostream>
#include "a_class.h"

int main(){
    using namespace std;
    Stock triority("Triority");
    triority.buy(114514, 3.1415926);
    triority.show();
    return 0;
}

```

如果要创建同一个类的多个对象，可以这样：
```c++
Stock stocks[4];
stocks[0].show();
```
如果使用构造函数则必须这样：
```c++
Stock stocks[2] = {
    Stock("a", 1.0, 1);
    Stock("b", 1.0, 1);
}
```

### this指针
在 C++ 中，this指针是一个特殊的指针，它指向当前对象的实例。每一个对象都能通过this指针来访问自己的地址。可以在类的成员函数中使用，可以用来指向调用对象。

当一个对象的成员函数被调用时，编译器会隐式地传递该对象的地址作为 this 指针。

通过使用 this 指针，我们可以在成员函数中访问当前对象的成员变量，即使它们与函数参数或局部变量同名，这样可以避免命名冲突，并确保我们访问的是正确的变量

```c++
#include <iostream>
 
class MyClass {
private:
    int value;
public:
    void setValue(int value) {
        this->value = value;
    }

    void printValue() {
        std::cout << "Value: " << this->value << std::endl;
    }
};

```

### 运算符重载
假设有一个Time类包含hours和minutes变量，求和的函数方法大概是这样
`time.h`
```c++
Time Time::Sum(const Time & t) const;
```
`time.cpp`
```c++
Time Time::Sum(const Time & t) const{
    Time sum;
    sum.minutes = minutes + t.minutes;
    sum.hours = hours + t.hours + sum.minutes/60
    sum.minutes %= 60;
    return sum;
}
```
如果要使用加法运算符进行这个操作，只需要把`Sum()`的名称改为`operator+()`即可
`time.h`
```c++
Time operator+(const Time & t) const;
```
`time.cpp`
```c++
Time operator+(const Time & t) const{
    Time sum;
    sum.minutes = minutes + t.minutes;
    sum.hours = hours + t.hours + sum.minutes/60
    sum.minutes %= 60;
    return sum;
}
```
此后计算时间总和就可以直接用`+`了
```c++
time_total = time_1 + time_2;
```

重载的使用有一些限制：
+ 重载后必须至少有一个操作数是用户定义的类型，避免用户为标准类型重载，比如重载`-`符号为求和
+ 不能修改运算符优先级
+ 重载不能违反原来的句法规则，比如将求模`%`重载成只用一个操作数
+ 不能创建新的运算符
+ 一些不能重载的运算符：`sizeof`等（懒得全写一遍了，这玩意估计八百年用不到一次）

### 友元
类对象的公有类发布方法是访问对象私有部分的唯一途径，但是这种限制有时候过于严格，因此提供了友元的概念，包括友元函数，友元类，友元成员函数。通过让函数成为类的友元可以赋予函数与类的成员函数相同的访问权限

在刚才的例子中可以实现时间的加法，那如果是乘法呢？由于运算符左侧是操作数，我们只能`A = B * double`而不能`A = double * B`，因为这个`double`不是对象。另一种解决方式就是使用友元

创建友元函数只要将其原型放在类声明中，并在前面加上`friend`关键字
```c++
friend Time operator*(double m, const Time & t);
```
显然这个函数在类声明中调用但是不是成员函数，但是拥有成员函数一样的访问权限

因为他不是成员函数，所以编写定义时不要使用`Time::`限定符，也不要使用关键字`friend`，应该这样：
```c++
Time operator*(double m, const Time & t){
    Time result;
    long totalminutes = t.hours *m * 60 + t.minutes * m;
    result.hours = totalminutes / 60;
    result.minutes = totalminutes % 60;
    return result;
}
```
有了这些声明和定义之后，就可以使用这一语句了：
```c++
Time_A = 2.75 * Time_B
```

### 类的自动转换和强制类型转换

c++会自动转换兼容的类型，比如`int a = 3.5;`会只保留整数部分，不兼容的类型不会自动转换，但是也许可以强制类型转换`int * p = (int *) 10;`，因为`p`和`(int *)`都是指针，虽然这样的转换大概率毫无意义

对于类，当构造函数只接受一个参数时（或者其他参数有默认值），可以编写这样的代码：
```c++
AClass(int a);

AClass aclass;
aclass = 100;
```
如果需要避免意外的这种转换，可以在声明构造函数时使用关键字`explicit`，从而关闭隐式转换，但仍然允许显式转换:
```c++
AClass aclass;
aclass = AClass(100);
//or
aclass = (AClass) 100;
```

转换函数可以反过来将类对象转换为一个值，这是一种用户定义的强制类型转换。要创建一个转换函数要注意，转换函数必须是类方法，不能指定返回类型，而且不能有参数。

```c++
//转换为double类型的函数的原型，添加到类的声明中
operator double();
//或者int，出于严谨也可以加入const
operator int() const;
```
然后在类定义中加入转换的方法（int返回double+0.5可以巧妙地四舍五入而不是丢弃小数部分）
```c++
AClass::operator int() const{
    return int (pounds + 0.5);
}
```
这样调用时候便可以直接使用
```c++
int a_int = aclass;
```
### 类和动态内存分配

使用`new`初始化对象的指针成员时应该注意一些事情：
+ 在构造函数中使用`new`初始化之后，应该在析构函数中使用`delete`，且必须互相兼容`new`对应`delete`且`new[]`对应于`delete[]`
+ 如果要进行对象的复制，应定义一个复制构造函数，进行实际内容的复制，而非指针。例如`b.str`是通过`new`创建的，类似`a.str = b.str`这样的直接复制只会复制地址，导致两个成员实际上指向同一份内容，并在当其中一个执行`delete`时导致数据损坏
+ 也应该定义一个赋值运算符，通过深度复制将一个对象复制给另一个对象。具体来说，应该首先检查自我赋值的情况，释放成员指针以前指向的内存，复制数据而不是地址，返回一个指向调用对象的引用

这部分内容可能比较难懂，需要一些举例才能完全理解，但是我现在又懒得在这补充一大堆代码作为举例，因此这件事交给未来的自己吧。在此之前可以直接阅读原书的P356

### 类的继承
假设已经有了下面这个类（由前面的例子删减而来）
`1.h`:
```c++
#include <string>

class Stock{
private:
    std::string company;
    long shares;
public:
    Stock(const std::string & co, long n = 0);
    void show() const;
    ~Stock();
};
```
`1.cpp`:
```c++
#include <iostream>
#include "1.h"

void Stock::show()const{
    std::cout << "Company:" << company << std::endl 
        << "Shares:" << shares << std::endl;
}

Stock::Stock(const std::string & co, long n){
    company = co;
    shares = n;
}

Stock::~Stock(){
    std::cout << "DEL " << company << std::endl;
}
```
我现在想要让这个类新增一个`id`成员，但是不想改动已有的代码（甚至可能没有源代码），那么可以直接派生出一个类：
`2.h`:
```c++
#include "1.h"
class Stock_id : public Stock{
private:
    long id;
public:
    Stock_id(long i, std::string co, long n = 0);
    void show_id() const;
};
```
`2.cpp`:
```c++
#include <iostream>
#include "2.h"

void Stock_id::show_id() const {
    std::cout << "id:" << id << std::endl;
    Stock_id::show();
}

Stock_id::Stock_id(long i, std::string co, long n) : Stock(co, n){
    id = i;
}
```
派生类需要自己的构造函数，也可以添加额外的数据成员和成员函数

但是注意不能直接访问基类的私有成员而必须通过基类方法进行访问，也就是说，`private`只能这个类自己访问，`protected`允许自己和派生类访问，`public`允许全部访问

派生类继承了所有的基类方法，但下列情况除外：基类的构造函数、析构函数和拷贝构造函数，基类的重载运算符，基类的友元函数。

### 多态继承

### 友元类

## 异常

```c++
#include <iostream>

int main(){
    double x,y,z;
    while(true){
        std::cout << "Enter 2 nums:";
        std::cin >> x >> y;
        try{
            if(y==0){
                throw "y = 0 is not allowed!";
            }
        }catch(const char * s){
            std::cout << s << std::endl;
            continue;
        }
        z = x/y;
        std::cout << "x / y is:" << z << std::endl;
    }
}
```
使用`try`捕获异常，然后在`catch()`中对异常进行处理，

{% note danger modern %}
这一部分原来书上的代码`catch (char* str)`运行会报错`terminate called after throwing an instance of 'char const*'`，这里是我改正且简化的版本。
原因是应该捕获const异常`catch (const char const* strException)`，[参考链接](https://stackoverflow.com/questions/24458563/throwing-exceptions-error-terminate-called)中还讨论了更加规范的错误处理方法和其他"style note: This tutorial smells, maybe you should find another source."😨😨😨
{% endnote %}




