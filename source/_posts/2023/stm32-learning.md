---
title: STM32学习笔记(STM32F103C8T6)
tags:
  - stm32
  - C语言
cover: /img/STM32F103C8T6.png
categories:
- 文档&笔记
date: 2023-09-11 14:49:06
description: STM32基础，以STM32F103C8T6最小系统板为例
---
# STM32简介及工具软件安装
## STM32简介
### 芯片命名及手册
![STM32F103C8T6是一款由意法半导体公司(ST)推出的基于Cortex-M3内核的32位微控制器，采用`LQFP48`封装](STM32F103C8T6.png)

![单片机命名规则](20210115142206386.png)

[STM32F103系列中文芯片手册](https://cr.triority.cn/f/1r0uP/STM32F103%E4%B8%AD%E6%96%87%E6%95%99%E7%A8%8B%E5%8F%8A%E5%8F%82%E8%80%83%E6%89%8B%E5%86%8C.pdf)

### 下载烧录
STM32单片机支持3种程序下载方式
+ ISP串口下载(使用USB-TTL接PA9、PA10)
+ SWD下载(使用ST-LINK接PA13、PA14)
+ JTAG下载(使用JLINK接PA13、PA14、PA15、PB3、PB4)

虽然有三种方式，但是我个人一般是使用st-link的，所以下面主要介绍这一个
#### ISP下载(串口)
使用ISP串口下载前，将单片机上电之前需要先用跳线帽把`BOOT0`短接到`1`的位置，`BOOT1`短接到`0`的位置，即系统存储器模式，然后才能通过串口下载程序。ISP串口下载完成后断电，在单片机上电之前需要先用跳线帽把`BOOT0`短接到`0`的位置，即主闪存存储器模式。

![启动模式](启动模式选择.png)

下载器GND与单片机GND相连，下载器3.3V与单片机3.3V相连(或者下载器5V与单片机VIN相连)、下载器RXD与单片机PA9(U1TX)相连，下载器TXD与单片机PA10(U1RX)相连

#### SWD下载(st-link)
使用SWD接口下载只需要连接3.3V、GND、`SWDIO(PA13)`、`SWCLK(PA14)`、`RST`(非必要)，可以从淘宝购买`ST-LINK`下载器。使用SWD接口除了可以烧录程序外，还可以实现在线仿真(debug)，仿真过程可以监视寄存器等数据，非常适合软件开发(找问题)。`ST-LINK/V2`只支持给自家的STM32和STM8烧录程序，不支持为其他公司的单片机烧录程序(即使同样搭载`Cortex-M3`内核)

如果使用`STLink`，其上的LED指示灯用于提示当前的工作状态：
+ LED 闪烁红色：`STLink`已经连接至计算机。
+ LED 保持红色：计算机已经成功与`STLink`建立通信连接。
+ LED 交替闪烁红色和绿色：数据正在传输。
+ LED 保持绿色：最后一次通信是成功的。
+ LED 为橘黄色：最后一次通信失败。

#### JTAG下载
这种方式很少使用，不再详细叙述

> 如果我们不需要使用JTAG下载，但GPIO资源紧张或PCB设计时已经使用了这些第一功能为JTAG的引脚，那么我们就需要关闭JTAG。比如说我要使用GPIOA15作为GPIO口，那么代码层面需要这样实现：
> ```c
>   GPIO_InitTypeDef GPIO_InitStructure;
>  	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_AFIO,ENABLE);//使能PORTA时钟
> 	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable , ENABLE);// 关闭JTAG但使能SWD
> 	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_15;//PA15
> 	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //设置上拉输入
> 	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
>  	GPIO_Init(GPIOA, &GPIO_InitStructure);//初始化GPIO
> ```

### 编程环境
#### 使用arduino编程
突然得知stm32可以用arduino编程，喜出望外hhh

添加开发板管理器地址
```
http://dan.drown.org/stm32duino/package_STM32duino_index.json
```
然后就可以找到`STM32F103C`来给我的板子编程了。


#### 使用keil编程
`Keil uVision`:编程工具，可以在官网注册获取下载链接，可能需要自行搜索破解，虽然不破解也能正常使用基础功能。
`STM32 ST-LINK Utility`：配套`ST-LINK`一起使用的烧录工具，包含`ST-Link`驱动，同样可以在官网下载，我也[copy的一份在网盘上](https://cr.triority.cn/f/2L8tv/STM32-ST-LINK-Utility-setup.exe)

其中如果使用后者进行下载而不是keil自带的下载按钮，需要设置keil编译后输出`.hex`文件：![设置生成hex文件](QQ截图20230511175030.png)

在`STM32 ST-LINK Utility`中，首先连接芯片`(Tarage -> connect或直接点击连接快捷按钮)`，然后打开`hex`文件`(也可以直接讲hex文件拖动到FLASH区域)`，最后就可以下载程序`(Taraget -> Program，也可以直接点击下载快捷按钮)`。弹出信息确认窗口，如hex文件路径、验证方式等，确认信息无误后点击`Start`开始下载程序，出现`Verification…OK`，说明下载成功。

# 编程：在keil环境下
## 新建工程
首先选择开发板芯片，我的是`stm32f103c8`

添加启动文件等，这部分文字说明比较麻烦(暂时懒得写了)，建议参考[这个视频](https://www.bilibili.com/video/BV1th411z7sn?p=4)

添加`main.c`文件，之后就可以在main文件中写代码了，写完可以编译一下，如果输出正确就表示环境配置没问题

## 基础操作
### GPIO高低电平输出
#### 磨磨唧唧的讲解
在GPIO输出之前要先对要操作的GPIO进行配置，下面这个程序可以连续将PC13这个引脚拉低拉高:

```c
# include "stm32f10x.h"
void LED_Init(void){
    //A
    GPIO_InitTypeDef GPIO_InitStructure;
    //B
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    //C
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    //D
    GPIO_Init(GPIOC, &GPIO_InitStructure);
}

int main(){
    LED_Init();
    while(1){
      //E
      GPIO_ResetBits(GPIOC,GPIO_Pin_13);
      GPIO_SetBits(GPIOC,GPIO_Pin_13);
    }
}
```
下面来解释一下这个程序:

> A:定义GPIO的初始化类型结构体

```c
GPIO_InitTypeDef GPIO_InitStructure;
```
此结构体的定义是在`stm32f10x_gpio.h`文件中，其中包括3个成员：
+ `uint16_t GPIO_Pin;`来指定GPIO的哪个或哪些引脚
+ `GPIOSpeed_TypeDef GPIO_Speed;`GPIO的速度配置,对应3个速度：10MHz、2MHz、50MHz
+ `GPIOMode_TypeDef GPIO_Mode;`为GPIO的工作模式配置，即GPIO的8种工作模式。
  + 输入浮空 `GPIO_Mode_IN_FLOATING`
  + 输入上拉 `GPIO_Mode_IPU`
  + 输入下拉 `GPIO_Mode_IPD`
  + 模拟输入 `GPIO_Mode_AIN`
  + 具有上拉或下拉功能的开漏输出 `GPIO_Mode_Out_OD`
  + 具有上拉或下拉功能的推挽输出 `GPIO_Mode_Out_PP`
  + 具有上拉或下拉功能的复用功能推挽 `GPIO_Mode_AF_PP`
  + 具有上拉或下拉功能的复用功能开漏 `GPIO_Mode_AF_OD`


> B:使能GPIO时钟

```c
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
```
此函数是在`stm32f10x_rcc.c`文件中定义的。其中第一个参数指要打开哪一组GPIO的时钟，取值参见`stm32f10x_rcc.h`文件中的宏定义，第二个参数为打开或关闭使能，取值参见`stm32f10x.h`文件中的定义，其中`ENABLE`代表开启使能，`DISABLE`代表关闭使能。
```c
void RCC_APB2PeriphClockCmd(uint32_t RCC_APB2Periph, FunctionalState NewState);
```


> C:设置`GPIO_InitTypeDef`结构体三个成员的值
```c
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
```


> D:初始化GPIO
```c
GPIO_Init(GPIOC, &GPIO_InitStructure);
```


> E:GPIO电平输出

函数就是置位GPIO，即让相应的GPIO输出高电平
```c
GPIO_ResetBits(GPIOC,GPIO_Pin_13);
GPIO_SetBits(GPIOC,GPIO_Pin_13);
```

很多网上找到的程序也会这样做，在文件开头写
```c
#define LED3_OFF GPIO_SetBits(GPIOB,GPIO_Pin_5)
#define LED3_ON GPIO_ResetBits(GPIOB,GPIO_Pin_5)
```
然后在调用时候就可以直接写
```c
LED3_ON;
LED3_OFF;
```

#### 直接上代码(LED闪烁)
```c
#include "stm32f10x.h"
#include "Delay.h"

int main(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    
    GPIO_Init(GPIOC, &GPIO_InitStructure);
    
    while(1){
        GPIO_WriteBit(GPIOC, GPIO_Pin_13, Bit_RESET);
        Delay_ms(500);
        GPIO_WriteBit(GPIOC, GPIO_Pin_13, Bit_SET);
        Delay_ms(500);
    }
}

```
这里面的延时函数来自[up江协科技](https://space.bilibili.com/383400717)
[Delay.c](Delay.c)
[Delay.h](Delay.h)

### GPIO输入
这一部分原理和上面几乎一样，通过`GPIO_ReadInputDataBit()`读取GPIO输入
```c
//初始化引脚
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

GPIO_InitTypeDef GPIO_InitStructure;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //IPU为输入模式
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1 | GPIO_Pin_11; //可以这样写同时设置多个引脚
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

GPIO_Init(GPIOB, &GPIO_InitStructure);

//读取引脚输入
if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)
	{
		Delay_ms(20);
		while (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0);
		Delay_ms(20);
		KeyNum = 1;
	}

```

此外，对于输出的引脚，也可以使用`GPIO_ReadOutputDataBit()`读取输出，比如这样翻转输出电平：
```c
void LED_Turn(void)
{
	if (GPIO_ReadOutputDataBit(GPIOA, GPIO_Pin_1) == 0){
		GPIO_SetBits(GPIOA, GPIO_Pin_1);
	}else{
		GPIO_ResetBits(GPIOA, GPIO_Pin_1);
	}
}
```
### 中断
中断涉及的结构如下图：
![](微信截图_20230911200344.png)
这一流程也就是我们配置中断的流程

#### 配置GPIO
```c
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
GPIO_InitTypeDef GPIO_InitStructure;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //上拉输入
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_Init(GPIOB, &GPIO_InitStructure);
```

#### 配置AFIO选择引脚
```c
RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);  //打开AFIO的时钟
GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource11);  //将11线路连接到B11
```

#### 配置EXTI
```c
EXTI_InitTypeDef EXTI_InitStructure;  //定义EXTI初始化结构体
EXTI_InitStructure.EXTI_Line = EXTI_Line11;
EXTI_InitStructure.EXTI_LineCmd = ENABLE; //使能
EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt; //事件模式或中断模式。这里选中断
EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling; //下降沿触发
EXTI_Init(&EXTI_InitStructure);
```
其中触发方式包含：
```c
//下降沿
EXTI_Trigger_Falling
//上升沿
EXTI_Trigger_Rising
//上升或下降
EXTI_Trigger_Rising_Falling
```

#### 配置NVIC
```c
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //中断分组，两位抢占优先级两位响应优先级
NVIC_InitTypeDef NVIC_InitStructure;  //定义NVIC初始化结构体
NVIC_InitStructure.NVIC_IRQChannel = EXTI15_10_IRQn;  //配置中断通道，EXITI10-15都在这个通道
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; //使能
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; //优先级设置为1
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;  //优先级设置为1
NVIC_Init(&NVIC_InitStructure);
```

#### 中断函数
stm32的中断函数名字是固定的，比如这里是EXTI15_10_IRQn通道的函数：
```c
void EXTI15_10_IRQHandler(void){
  //首先判断标志位，确定是11线路的信号
  if (EXTI_GetITStatus(EXTI_Line11) == SET){
    //执行的程序

    //清除中断标志位，退出中断。注意如果不清除将会不停申请中断导致卡死
    EXTI_ClearITPendingBit(EXTI_Line11);
  }
}
```

#### 实例
这个程序可以实现PB11下降沿中断时反转PC13引脚的输出：
```c
#include "stm32f10x.h"

int main(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);
    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
    
    GPIO_InitTypeDef GPIO_InitStructure2;
    GPIO_InitStructure2.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure2.GPIO_Pin = GPIO_Pin_11;
    GPIO_InitStructure2.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure2);
    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);  //打开AFIO的时钟
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource11);  //将11线路连接到B11
    
    EXTI_InitTypeDef EXTI_InitStructure;  //定义EXTI初始化结构体
    EXTI_InitStructure.EXTI_Line = EXTI_Line11;
    EXTI_InitStructure.EXTI_LineCmd = ENABLE; //使能
    EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt; //事件模式或中断模式。这里选中断
    EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling; //下降沿触发
    EXTI_Init(&EXTI_InitStructure);
    
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //中断分组，两位抢占优先级两位响应优先级
    NVIC_InitTypeDef NVIC_InitStructure;  //定义NVIC初始化结构体
    NVIC_InitStructure.NVIC_IRQChannel = EXTI15_10_IRQn;  //配置中断通道，EXITI10-15都在这个通道
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; //使能
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; //优先级设置为1
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;  //优先级设置为1
    NVIC_Init(&NVIC_InitStructure);
    
    
    while(1){}
}

void EXTI15_10_IRQHandler(void){
  if (EXTI_GetITStatus(EXTI_Line11) == SET){
    //执行的程序
	if (GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13) == 0){
		GPIO_SetBits(GPIOC, GPIO_Pin_13);
	}else{
		GPIO_ResetBits(GPIOC, GPIO_Pin_13);
	}
    
    EXTI_ClearITPendingBit(EXTI_Line11);
  }
}

```

### 定时器
#### 定时中断
定时中断基本结构:
![定时中断基本结构](QQ截图20230913003026.png)
##### 操作流程
```c
RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);  //tim2是APB1总线的外设，开启时钟

TIM_InternalClockConfig(TIM2);  //设置时基单元时钟为内部时钟，默认值也是这个所以其实可以不写

TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;  //定义时基单元初始化结构体
TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1; //时钟滤波器时钟分频，1表示不分频，还可以是2和4
TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; //计数模式，这里是向上计数
TIM_TimeBaseInitStructure.TIM_Period = 10000 - 1; //计数器，10k频率计数1w也即是1s定时，数值必须位于0-65535
TIM_TimeBaseInitStructure.TIM_Prescaler = 7200 - 1; //预分频器，对72M分频7200得到10k频率，数值必须位于0-65535
TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;  //重复计数器，仅高级计时器有，所以直接配置0
TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);

TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);  //tim2的更新中断使能，使信号通往NVIC

//NVIC配置，上一节讲过了
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
NVIC_InitTypeDef NVIC_InitStructure;
NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn; //tim2的通道
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
NVIC_Init(&NVIC_InitStructure);

TIM_Cmd(TIM2, ENABLE);  //使能定时器
```
下面是中断函数
```c
void TIM2_IRQHandler(void){
	if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET){
		//做点东西

    //清除标志位
		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
	}
}

```
##### 代码操作
这个程序可以让PC13每秒亮灭一次
```c
#include "stm32f10x.h"

int main(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);
    
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    
    TIM_InternalClockConfig(TIM2);
    
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
    TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up;
    TIM_TimeBaseInitStructure.TIM_Period = 10000 - 1;
    TIM_TimeBaseInitStructure.TIM_Prescaler = 7200 - 1;
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;
    TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);
    
    TIM_ClearFlag(TIM2, TIM_FLAG_Update); //这个函数上面没讲。因为上电启动会直接触发中断以更新配置，这样写可以避免上电立刻触发中断
    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
    
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    
    NVIC_InitTypeDef NVIC_InitStructure;
    NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_Init(&NVIC_InitStructure);
    
    TIM_Cmd(TIM2, ENABLE);
    
    while(1){}
}

void TIM2_IRQHandler(void){
    if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET){
        if (GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13) == 0){
            GPIO_SetBits(GPIOC, GPIO_Pin_13);
        }else{
            GPIO_ResetBits(GPIOC, GPIO_Pin_13);
        }
        TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
    }
}

```
#### PWM输出
![](微信截图_20230913111001.png)

定时器配置和上一节一样，只不过不需要中断配置了

```c
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
// 这部分注释表示引脚重映射，默认tim2定时器的输出引脚是PA0，注释这部分可以重映射到PA15，当然下面GPIO_Pin_0也要改成注释的GPIO_Pin_15
//	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);  //打开AFIO
//	GPIO_PinRemapConfig(GPIO_PartialRemap1_TIM2, ENABLE); //打开部分重映射1
//	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable, ENABLE);  //PA15默认复用为调试端口，关闭JTAG功能即可作为普通GPIO，但是务必保留SWJ否则无法再使用st-link下载程序
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;		//GPIO_Pin_15;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	TIM_InternalClockConfig(TIM2);
	
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;
	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up;
	TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;		//ARR，输出1k
	TIM_TimeBaseInitStructure.TIM_Prescaler = 720 - 1;		//PSC，分频到100k
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);
	//这里上面的都和之前一样

	TIM_OCInitTypeDef TIM_OCInitStructure;  //定义配置结构体
	TIM_OCStructInit(&TIM_OCInitStructure); //初始化结构体。下面几个参数是通用定时器的参数，还有一些没用到的参数这样可以初始化配置，如果未来改成高级定时器不至于出错
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1; //输出比较模式
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High; //输出比较极性
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; //输出使能
	TIM_OCInitStructure.TIM_Pulse = 0;		//CCR
	TIM_OC1Init(TIM2, &TIM_OCInitStructure);  //输出比较器配置，使用通道为OC1
	
	TIM_Cmd(TIM2, ENABLE);
```

之后修改pwm占空比就可以使用这个函数：Compare为CCR
```c
TIM_SetCompare1(TIM2, Compare);
```

#### TIM输入捕获

### 串口通讯
