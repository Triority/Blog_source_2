---
title: 在vscode中使用c语言开发raspberry-pico
tags:
  - 树莓派
  - 单片机
  - C语言
cover: /img/RUN.png
categories:
  - 折腾记录
date: 2024-05-15 16:12:39
description: pico好c坏
---
# 工具链环境安装
## 环境配置
[官方教程](https://www.raspberrypi.com/news/raspberry-pi-pico-windows-installer/)

[安装程序仓库](https://github.com/raspberrypi/pico-setup-windows)

在仓库readme中[Download the latest release](https://github.com/raspberrypi/pico-setup-windows/releases/latest/download/pico-setup-windows-x64-standalone.exe)

程序安装完成后，打开位于开始菜单的`Raspberry Pi Pico SDK v1.5.1`文件夹，运行里面的`Pico - Visual Studio Code`。会自动启动vscode打开保存在我的文档中的`pico-examples`文件夹，并询问使用的编译设置，选择`带有 GCC arm-none-eabi 条目的 Pico ARM GCC - Pico SDK 工具链`。

添加环境变量：

| 变量名 | 变量值 |
| - | - |
| `PICO_SDK_PATH` | `C:\Program Files\Raspberry Pi\Pico SDK v1.5.1\pico-sdk` |
| `PICO_EXAMPLES_PATH` | `C:\Users\Triority\Documents\Pico-v1.5.1\pico-examples` |

## 新建工程
新建文件夹，打开`powershell`：
```powershell
copy ${env:PICO_SDK_PATH}\external\pico_sdk_import.cmake .

copy ${env:PICO_EXAMPLES_PATH}\.vscode . -recurse
```
新建一个`CMakeLists.txt`：
```t
cmake_minimum_required(VERSION 3.13)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(my_project)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

# rest of your project

```

About the simplest you can do is a single source file (e.g. hello_world.c)：
```c
#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    setup_default_uart();
    printf("Hello, world!\n");
    return 0;
}
```

添加到`CMakeLists.txt`文件的末尾：
```t
add_executable(hello_world
    hello_world.c
)

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(hello_world pico_stdlib)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(hello_world)
```

在开始菜单的`Pico - Visual Studio Code`打开刚才的文件夹即可，点击左下角的生成，会询问编译器配置，直接选择之前一样的`Pico ARM GCC - Pico SDK Toolchain with GCC arm-none-eabi entry`，如果编译成功到此配置完成

# 开发
