---
title: 一个“比较”亮的手电
tags:
  - 电力电子
  - PCB设计
  - stm32
#cover: /img/标题图做完再加
categories:
  - 折腾记录
date: 2024-12-10 13:13:13
description: 手电筒，但是500W，70000lm
---
# 想法
做这个的想法大部分来源于有一天晚上，走G6辅路从昌平骑车回市内，一堆解限速横冲直撞的逆行远光电动车给我整破防了，想做个小手电制裁一下。起因只是这么简单但是考虑到其他无辜的人我也不会真的这样去做，但是发现这个东西好像确实需要，用来摄影打光，以及夜间外出徒步这类活动都可以用，所以还是决定做出来

另一方面，关于这个手电的电源。绝大部分的设计方案都是使用一颗升压芯片来做电源控制，但是我这里有些别的想法。我以后会做一个大功率自动升降压可调电源，正好可以在这里复用，就当提前踩个坑了，所以虽然会更贵一点，我决定供电方案采用buck-boost自动升降压的恒定电流控制，顺便兼容一下各种电压的电池。（来自2025年的补充：考虑到复刻可行性和成本因素还是决定用boost恒流）

至于控制芯片，考虑到这个功能不算复杂，以及我想拿stm32但是用的机会不多，就用stm32f103c8t6做主控吧

# 设计方案
## 硬件
### LED

<details>
  <summary>隐藏内容：已被抛弃的大力转飞但是高效率方案（很难想象这两个形容词放在了一起）</summary>
  这部分没啥技术含量，找个光效高功率大的灯就完了，这里我选择了立德达的5050贴片LED，光效250lm/w，显色指数70，电压选择了6V。随手画一个2串50并的铝基板灯板。按照规格书的功率最大值，单个功率3W，光通量700lm，总计12V 25A 300W功率，70000流明。

  | ![](微信截图_20241210150050.png) | ![](微信截图_20241210150036.png) |
  |:---:|:---:|
  | [原理图](ProDoc_P1_2024-12-10.epro) | [PCB](ProDoc_PCB1_(6V)_2024-12-10.epro) |
  | <img width=2000/> | <img width=2000/> |

  但是这样有个问题，发光面积过大导致光强过低，因此后来没有采用这一方案。关于冷却方案，原计划~~直接上水冷！冷头使用60x60mm的铝制水冷头，搭配150x40x40的服务器冷排，在手电筒的体积内散热400W已经完全足够了。为了体积也不打算要水箱了，水泵随手买了个5V供电的微型水泵~~ 但是考虑到体积因素还是风冷了

  这一方案需要电压为12V，考虑到电池为3s电压因此供电采用buck-boost拓扑，这一部分也进行了matlab仿真设计，可惜在这里用不到了。仿真条件：电阻1Ω，输入电压12V，输出电容110uf，ESR10mΩ，电感33uH，开关频率100kHz，半桥PWM占空比最大值95%。[matlab simulink仿真文件](buckboost.slx)

  | ![](微信截图_20250222224440.png) | ![](微信截图_20250222224225.png) | ![](微信截图_20250222224422.png) |
  |:---:|:---:|:---:|
  | 5A恒流输出 | 10A恒流输出 | 20A恒流输出 |
  | <img width=2000/> | <img width=2000/> | <img width=2000/> |

  甚至还画了一个boost电路但是WDDQQX把mos橄榄了没有用得上

  | ![](微信截图_20250222223801.png) | ![](微信截图_20250222223834.png) |
  |:---:|:---:|
  | 原理图 | 3D-PCB |
  | <img width=2000/> | <img width=2000/> |

</details>

综合发光面积、价格、效率等，最终选择SFY55灯珠，参数如下：

| ![](69bd46e38601a5c39a4775097e952c4.jpg) | ![](9e2aa0a23079d13a982fd5dbf028188.jpg) | ![](357dc85888bb8805679a9b63933a9be.jpg) | ![](49928d9e79ca2d41cbe7b6165ae1758.jpg) | ![](617e2a1d9a860104e65897fc72a1f42.jpg) |
|:---:|:---:|:---:|:---:|:---:|
| 外形尺寸 | 光通量-电功率 | 光通量-电流 | 伏安特性曲线 | CCT色温-电流 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> | <img width=2000/> | <img width=2000/> |

这款灯珠为国产型号，虽然光效较低（但考虑人眼对数感知特性这点效率也问题不大）但是价格便宜，而且功率密度足够。上面加上反光杯进一步增加光强。

### 制冷
散热方案极其重要，工作温度直接影响到灯珠功率效率和寿命。考虑体积没有采用水冷，而是使用了下压式风冷CPU散热器。虽然远超出了此类散热器的标称功率，但是更换风扇为台达9cm 12V 4.32A暴力风扇后完美解决（别问噪音，问就没有）

![](535a78305d36408756ae3cecb5cfe69.jpg)

### 供电
灯珠供电需要恒流控制下的大约24V电压，正常情况下电流需要20A.以及最高12V可调供电给散热风扇，3.3V给主控电路，外围这部分直接用buck降压电路和LDO芯片解决了没啥可说的。

#### 恒流boost电路
##### v3驱动板设计


##### v2驱动板设计
| ![](微信截图_20250730214721.png) | ![](微信截图_20250730214705.png) | ![](fe65e89473042650ebb57acb621e241.jpg) |
|:---:|:---:|:---:|
| [原理图](ProDoc_P1_2025-07-30.epro) | [PCB](ProDoc_PCB3_2025-07-30.epro) | 实物 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> |

实验效果较好：信号线路工作正常，无电磁干扰影响，实现恒流控制。

存在的问题：风扇未知原因无法启动，断开信号线连接仅接入电源可以启动；逐渐加大电流过程中mos烧毁(200w+)；芯片短路保护控制引脚电压过低，短接后级放大电路强行上拉mos栅极才能工作。

增大功率过程中mos发热严重，换用TO-220封装的并联折角加散热片焊上去测试可以正常工作到30%电流：

| ![](8a17e114a10a43199fff09d865ebc15.jpg) | ![](751b88d810fcca3590ff2f78bb0068c.jpg) | ![](c0fa337e340a19501c9705a8f6f66f8.jpg) |
|:---:|:---:|:---:|
| 20%电流工作情况 | Vgs波形 | Vds波形 |
| <img width=2000/> | <img width=2000/> | <img width=2000/> |

综上，下一个版本要做的改进:
1. 散热风扇测速信号导致错误
2. 更换电感值同时降低mosfet开关频率
3. stm32的电流检测分辨率不足，要加个运算放大器
4. 更换mosfet封装和散热
5. 风扇电源应内部稳压而非直连电源以满足宽电压要求
6. 栅极电阻改用3.3欧
7. 芯片ldo电容改用1uf

##### v1驱动板设计
基本无法正常工作，信号反馈回路遭遇严重电磁干扰。设计就不在这放了，主要是PCB设计的问题

## 软件

![](微信截图_20250730222639.png)
[cubemx设计](Light.zip)

stm32:keil main.c
```c
/* USER CODE BEGIN Header */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "ssd1306.h"
#include "stdio.h"
#include "Delay.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
int ERR = 0;
char bufnum[7];
volatile uint16_t ADC_Value[9];
uint16_t ADC_Vout,ADC_Fb,ADC_Vin,ADC_TEMP0,ADC_TEMP1,ADC_KNOB0,ADC_KNOB1,ADC_SW,ADC_TEMPSTM;
float Vout,Iout,Vin,TEMP0,TEMP1,KNOB0,KNOB1,SW,TEMPSTM;
int status_SW,status_KNOB;
int DIM_9209;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_I2C1_Init();
  MX_USART1_UART_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  /* USER CODE BEGIN 2 */
	HAL_TIM_Base_Start_IT(&htim3);
	HAL_TIM_PWM_Start (&htim2,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start (&htim2,TIM_CHANNEL_2);
	HAL_ADC_Start_DMA(&hadc1, (uint32_t*)&ADC_Value, 9);
	
	SSD1306_Init ();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	

	
	while (1)
  {
		//EN
		if(ERR||status_SW==1){
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4, GPIO_PIN_RESET);
		}else{
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4, GPIO_PIN_SET);
		}
		//ADC
		ADC_Vout=ADC_Value[0];
		ADC_Fb=ADC_Value[1];
		ADC_Vin=ADC_Value[2];
		ADC_TEMP0=ADC_Value[3];
		ADC_TEMP1=ADC_Value[4];
		ADC_KNOB0=ADC_Value[5];
		ADC_KNOB1=ADC_Value[6];
		ADC_SW=ADC_Value[7];
		ADC_TEMPSTM=ADC_Value[8];
		Vout=(float)ADC_Vout * 3.3f * 11.0f/ 4095.0f;
		Iout=(float)ADC_Fb * 3.3f / 0.0125f / 4095.0f;
		Vin=(float)ADC_Vin * 3.3f * 11.0f / 4095.0f;
		TEMP0=(float)ADC_TEMP0 * 3.3f / 4095.0f;
		TEMP1=(float)ADC_TEMP1 * 3.3f / 4095.0f;
		KNOB0=(float)ADC_KNOB0 / 4095.0f;
		KNOB1=(float)ADC_KNOB1 / 4095.0f;
		SW=(float)ADC_SW / 4095.0f;
		TEMPSTM=(1.43f - ((float)ADC_TEMPSTM * 3.3f / 4095.0f))/0.0043f + 25.0f;
		//status
		status_KNOB = (int)(KNOB0*20)*10+(int)(KNOB1*20.0f);
		if(status_KNOB>100)status_KNOB=100;
		if(SW>0.66f){status_SW=2;}else if(SW>0.33f){status_SW=1;}else{status_SW=0;}
		//DIM pwm
		DIM_9209 = 10 + status_KNOB*989/100;
		__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, DIM_9209);
		
		
	}
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV6;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim){
	  if(htim == &htim3)
	 {
	    HAL_GPIO_TogglePin(GPIOC,GPIO_PIN_13);
		 //oled
		  SSD1306_GotoXY (0,0);
			sprintf (bufnum, "PWM%03d", DIM_9209);
			SSD1306_Puts (bufnum, &Font_11x18, 1);
			SSD1306_GotoXY (0,20);
			sprintf (bufnum, "Vo:%03.1f", Vout);
			SSD1306_Puts (bufnum, &Font_11x18, 1);
			SSD1306_GotoXY (0,40);
			sprintf (bufnum, "Io:%03.1f", Iout);
			SSD1306_Puts (bufnum, &Font_11x18, 1);
			SSD1306_UpdateScreen();
	 }
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

```


# 成品

