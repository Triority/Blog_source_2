---
title: 天气预报
date: 2022-4-29 02:13:28
tags:
- python
description: 使用和风天气api获取天气并发送邮件
cover: /img/hp-feat-data.png
categories: 
- 折腾记录
---
## 简介
城市代号可以在这个网址查看:https://where.qweather.com/index.html
邮箱自动发送需要填写你的授权密码send_pass!
获得密钥key请访问下面网站注册账号并获取web-api应用的密钥https://dev.qweather.com
## 代码
### 使用QQ邮箱
不要问为什么是list-for问就是我也不知道
```python
import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
key='xxxxxxxxxxxxxxxxxxxxxxxxx'

list = [["12345@qq.com",'100000','Triority']
]

def send(msg,rec_user):
    mail_host="smtp.qq.com"
    send_user="12345@qq.com"
    send_pass="pass"
    message=MIMEText(msg,'plain','utf-8')
    message['from']=Header(send_user,'utf-8')
    message['to']=Header(rec_user,'utf-8')
    subject='今日份天气预报来咯'
    message['Subject']=Header(subject,'utf-8')
    try:
        smtpObj=smtplib.SMTP_SSL(mail_host,465)
        smtpObj.login(send_user,send_pass)
        smtpObj.sendmail(send_user,rec_user,message.as_string())
        print('succeed')
    except smtplib.SMTPException:
        print('error')


def get_time():
    tim=time.localtime(time.time())
    tm_year=tim[0]
    tm_mon=tim[1]
    tm_mday=tim[2]
    tm_hour=tim[3]
    tm_min=tim[4]
    tm_yday = tim[7]
    return tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday


def now_weather(key,location):
    url='https://devapi.qweather.com/v7/weather/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    now_temp = now_res_json['now']['temp']#温度
    now_feelsLike = now_res_json['now']['feelsLike']#体感温度
    now_windScale = now_res_json['now']['windScale']#风力等级
    now_windSpeed = now_res_json['now']['windSpeed']#风速
    now_windDir = now_res_json['now']['windDir']#风向
    now_text = now_res_json['now']['text']#描述
    now_obsTime = now_res_json['now']['obsTime']#观测时间
    return now_temp,now_feelsLike,now_windScale,now_windSpeed,now_windDir,now_text,now_obsTime


def today_weather(key,location):
    url='https://devapi.qweather.com/v7/weather/3d?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    sunrise = now_res_json['daily'][0]['sunrise']#日出时间
    sunset = now_res_json['daily'][0]['sunset']#日落时间
    moonrise = now_res_json['daily'][0]['moonrise']#月升时间
    moonset = now_res_json['daily'][0]['moonset']#月落时间
    tempMax = now_res_json['daily'][0]['tempMax']#当天最高温度
    tempMin = now_res_json['daily'][0]['tempMin']#当天最低温度
    textDay = now_res_json['daily'][0]['textDay']#白天天气状况
    textNight = now_res_json['daily'][0]['textNight']#晚间天气状况
    windDirDay = now_res_json['daily'][0]['windDirDay']#白天风向
    windScaleDay = now_res_json['daily'][0]['windScaleDay']#白天风力等级
    windSpeedDay = now_res_json['daily'][0]['windSpeedDay']#白天风速
    precip = now_res_json['daily'][0]['precip']#当天总降水量
    uvIndex = now_res_json['daily'][0]['uvIndex']#紫外线强度指数
    humidity = now_res_json['daily'][0]['humidity']#相对湿度
    return sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay, windScaleDay, windSpeedDay, precip, uvIndex, humidity


def now_air(key,location):
    url='https://devapi.qweather.com/v7/air/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    category = now_res_json['now']['category']#空气质量指数级别
    aqi = now_res_json['now']['aqi']#空气质量指数
    return category, aqi

def txt(key,location,name):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday = get_time()
    now_temp, now_feelsLike, now_windScale, now_windSpeed, now_windDir, now_text, now_obsTime = now_weather(key,location)
    sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay,  windScaleDay, windSpeedDay, precip, uvIndex, humidity = today_weather(key,location)
    category, aqi = now_air(key,location)
    msg ='''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>HTML Editor - LDDGO.NET</title>
</head>
<body>
<p><span style="font-size: 14pt;">Dear '''+name+''':</span></p>
<p><span style="font-size: 12pt;">早安!</span></p>
<p><span style="font-size: 12pt;">今天是'''+str(tm_year)+'''年'''+str(tm_mon)+'''月'''+str(tm_mday)+'''日,是今年的第'''+str(tm_yday)+'''天了哦</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">下面是现在实时的天气状况:</span></p>
<p><span style="font-size: 12pt;">现在室外的空气状况为'''+category+''',质量指数为'''+aqi+'''</span></p>
<p><span style="font-size: 12pt;">今天早上天气'''+now_text+''',气温'''+now_temp+'''度,体感温度'''+now_feelsLike+'''度,</span></p>
<p><span style="font-size: 12pt;">刮'''+now_windDir+''',风力'''+now_windScale+'''级,速度约'''+now_windSpeed+'''m/s</span></p>
<p><span style="font-size: 12pt;">以上信息的测量时间为'''+now_obsTime+'''</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">下面是今天全天的天气情况:</span></p>
<p><span style="font-size: 12pt;">今天白天天气'''+textDay+''',最低气温是'''+tempMin+'''度,最高'''+tempMax+'''度,</span></p>
<p><span style="font-size: 12pt;">刮'''+windDirDay+''',风力'''+windScaleDay+'''级,速度约'''+windSpeedDay+'''m/s</span></p>
<p><span style="font-size: 12pt;">预计今天总降水量为'''+precip+'''毫米,紫外线指数'''+uvIndex+''',相对湿度为'''+humidity+'''.</span></p>
<p><span style="font-size: 12pt;">今天的日出时间是:'''+sunrise+''',日落时间:'''+sunset+''',月亮在'''+moonrise+'''升起,在'''+moonset+'''落下,</span></p>
<p><span style="font-size: 12pt;">今天夜晚天气'''+textNight+'''</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">Sincerely wish you all the best of luck today !!!</span></p>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="font-size: 12pt;">Triority</span></p>
<p style="text-align: right;"><span style="font-size: 12pt;">'''+str(tm_year)+'''.'''+str(tm_mon)+'''.'''+str(tm_mday)+'''</span></p>
</body>
</html>
    '''
    return msg



for i in list:
    send(txt(key, i[1], i[2]), i[0])
```

### 使用自建邮箱
这一段是半年之后才想起来写的，已经不记得当初为什么要改代码了，但是既然改了在这也留一份吧
后来搭建了自己的邮箱系统，用`triority@triority.cn`这个地址发送，代码改成了这样：
```python
import requests
import time
key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
list = [["xxx@qq.com", '100000','Triority']
        ]


def send_mail(mail_from, password, mail_to, subject, content, subtype=None):
    url = 'http://triority.cn:8888/mail_sys/send_mail_http.json'
    pdata = {}
    pdata['mail_from'] = mail_from
    pdata['password'] = password
    pdata['mail_to'] = mail_to
    pdata['subject'] = subject
    pdata['content'] = content
    pdata['subtype'] = subtype
    resp_data = requests.post(url, pdata).json()
    print(mail_to+str(resp_data))


def get_time():
    tim=time.localtime(time.time())
    tm_year = tim[0]
    tm_mon = tim[1]
    tm_mday = tim[2]
    tm_hour = tim[3]
    tm_min = tim[4]
    tm_yday = tim[7]
    return tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday


def now_weather(key, location):
    url='https://devapi.qweather.com/v7/weather/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    now_temp = now_res_json['now']['temp']#温度
    now_feelsLike = now_res_json['now']['feelsLike']#体感温度
    now_windScale = now_res_json['now']['windScale']#风力等级
    now_windSpeed = now_res_json['now']['windSpeed']#风速
    now_windDir = now_res_json['now']['windDir']#风向
    now_text = now_res_json['now']['text']#描述
    now_obsTime = now_res_json['now']['obsTime']#观测时间
    return now_temp,now_feelsLike,now_windScale,now_windSpeed,now_windDir,now_text,now_obsTime


def today_weather(key,location):
    url='https://devapi.qweather.com/v7/weather/3d?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    sunrise = now_res_json['daily'][0]['sunrise']#日出时间
    sunset = now_res_json['daily'][0]['sunset']#日落时间
    moonrise = now_res_json['daily'][0]['moonrise']#月升时间
    moonset = now_res_json['daily'][0]['moonset']#月落时间
    tempMax = now_res_json['daily'][0]['tempMax']#当天最高温度
    tempMin = now_res_json['daily'][0]['tempMin']#当天最低温度
    textDay = now_res_json['daily'][0]['textDay']#白天天气状况
    textNight = now_res_json['daily'][0]['textNight']#晚间天气状况
    windDirDay = now_res_json['daily'][0]['windDirDay']#白天风向
    windScaleDay = now_res_json['daily'][0]['windScaleDay']#白天风力等级
    windSpeedDay = now_res_json['daily'][0]['windSpeedDay']#白天风速
    precip = now_res_json['daily'][0]['precip']#当天总降水量
    uvIndex = now_res_json['daily'][0]['uvIndex']#紫外线强度指数
    humidity = now_res_json['daily'][0]['humidity']#相对湿度
    return sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay, windScaleDay, windSpeedDay, precip, uvIndex, humidity


def now_air(key,location):
    url='https://devapi.qweather.com/v7/air/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    category = now_res_json['now']['category']#空气质量指数级别
    aqi = now_res_json['now']['aqi']#空气质量指数
    return category, aqi


def txt(key,location,name):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday = get_time()
    now_temp, now_feelsLike, now_windScale, now_windSpeed, now_windDir, now_text, now_obsTime = now_weather(key,location)
    sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay,  windScaleDay, windSpeedDay, precip, uvIndex, humidity = today_weather(key,location)
    category, aqi = now_air(key,location)
    msg ='''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>HTML Editor - LDDGO.NET</title>
</head>
<body>
<p><span style="font-size: 14pt;">Dear '''+name+''':</span></p>
<p><span style="font-size: 12pt;">早安!</span></p>
<p><span style="font-size: 12pt;">今天是'''+str(tm_year)+'''年'''+str(tm_mon)+'''月'''+str(tm_mday)+'''日,是今年的第'''+str(tm_yday)+'''天了哦</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">下面是现在实时的天气状况:</span></p>
<p><span style="font-size: 12pt;">现在室外的空气状况为'''+category+''',质量指数为'''+aqi+'''</span></p>
<p><span style="font-size: 12pt;">今天早上天气'''+now_text+''',气温'''+now_temp+'''度,体感温度'''+now_feelsLike+'''度,</span></p>
<p><span style="font-size: 12pt;">刮'''+now_windDir+''',风力'''+now_windScale+'''级,速度约'''+now_windSpeed+'''m/s</span></p>
<p><span style="font-size: 12pt;">以上信息的测量时间为'''+now_obsTime+'''</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">下面是今天全天的天气情况:</span></p>
<p><span style="font-size: 12pt;">今天白天天气'''+textDay+''',最低气温是'''+tempMin+'''度,最高'''+tempMax+'''度,</span></p>
<p><span style="font-size: 12pt;">刮'''+windDirDay+''',风力'''+windScaleDay+'''级,速度约'''+windSpeedDay+'''m/s</span></p>
<p><span style="font-size: 12pt;">预计今天总降水量为'''+precip+'''毫米,紫外线指数'''+uvIndex+''',相对湿度为'''+humidity+'''.</span></p>
<p><span style="font-size: 12pt;">今天的日出时间是:'''+sunrise+''',日落时间:'''+sunset+''',月亮在'''+moonrise+'''升起,在'''+moonset+'''落下,</span></p>
<p><span style="font-size: 12pt;">今天夜晚天气'''+textNight+'''</span></p>
<p>&nbsp;</p>
<p><span style="font-size: 12pt;">Sincerely wish you all the best of luck today !!!</span></p>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="font-size: 12pt;">Triority</span></p>
<p style="text-align: right;"><span style="font-size: 12pt;">'''+str(tm_year)+'''.'''+str(tm_mon)+'''.'''+str(tm_mday)+'''</span></p>
</body>
</html>
    '''
    return msg


if __name__ == '__main__':
    for i in list:
        mail_from = 'triority@triority.cn'
        password = 'xxxxxxxxxxxx'
        mail_to = i[0]
        subject = '今日天气预报'
        content = txt(key,i[1],i[2])
        subtype = 'html'
        send_mail(mail_from, password, mail_to, subject, content, subtype)

```