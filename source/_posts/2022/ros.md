---
title: ros学习笔记
date: 2022-02-01 15:55:02
tags:
- 笔记
- linux
- python
- ROS
categories: 
- 文档&笔记
cover: /img/ros.png
description: ros学习知识整理和过程记录
---

## 工作空间和功能包
### 工作空间
#### 主要结构
1.代码空间src
2.编译空间build
3.开发空间devel
4.安装空间install
#### 基本操作
```
#创建代码空间
mkdir src
#进入代码空间
cd src
#创建工作空间
catkin_init_workspace
#回到上一级
cd ..
#编译
catkin_make
#生成install空间
catkin_make install
```
#### 环境变量
```
#设置环境变量
source devel/setup.bash
#检查环境变量
echo $ROS_PACKAGE_PATH
```
如果不想每次设置也可以修改`/home/triority`内的文件`.bashrc`，
在`source /opt/ros/melodic/setup.bash`下一行加入:
`source /home/triority/桌面/ROS_learning/devel/setup.bash`
### 创建功能包
在`src`文件夹内：
```
catkin_create_pkg <包名> <依赖>
```
```
#创建依赖roscpp[用于编写c++程序],rospy[用于编写python程序],std_msgs[ros标准消息结构]等依赖的的一个名为learning的功能包[应创建在src文件夹内]
catkin_create_pkg learning roscpp rospy std_msgs geometry_msgs turtlesim message_generation
```
## 话题：发布与订阅
### Publisher
##### 功能包代码
在learning功能包内新建`scripts`文件夹，创建python文件：
代码来自古月居
velocity_publisher.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将发布turtle1/cmd_vel话题，消息类型geometry_msgs::Twist

import rospy
from geometry_msgs.msg import Twist

def velocity_publisher():
	# ROS节点初始化
    rospy.init_node('velocity_publisher', anonymous=True)

	# 创建一个Publisher，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，队列长度10
    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

	#设置循环的频率
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
		# 初始化geometry_msgs::Twist类型的消息
        vel_msg = Twist()
        vel_msg.linear.x = 0.5
        vel_msg.angular.z = 0.2

		# 发布消息
        turtle_vel_pub.publish(vel_msg)
    	rospy.loginfo("Publsh turtle velocity command[%0.2f m/s, %0.2f rad/s]", 
				vel_msg.linear.x, vel_msg.angular.z)

		# 按照循环频率延时
        rate.sleep()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
```
##### 执行
启动ROS Master
```
roscore
```
打开海龟仿真器
```
rosrun turtlesim turtlesim_node
```
启动publisher
```
rosrun learning velocity_publisher.py
```
然后就能看见海龟开始做圆周运动。
### Subscriber
##### 功能包代码
在`scripts`文件夹内，创建python文件：
代码来自古月居
pose_subscriber.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将订阅/turtle1/pose话题，消息类型turtlesim::Pose

import rospy
from turtlesim.msg import Pose

def poseCallback(msg):
    rospy.loginfo("Turtle pose: x:%0.6f, y:%0.6f", msg.x, msg.y)

def pose_subscriber():
	# ROS节点初始化
    rospy.init_node('pose_subscriber', anonymous=True)

	# 创建一个Subscriber，订阅名为/turtle1/pose的topic，注册回调函数poseCallback
    rospy.Subscriber("/turtle1/pose", Pose, poseCallback)

	# 循环等待回调函数
    rospy.spin()

if __name__ == '__main__':
    pose_subscriber()
```
##### 执行
启动ROS Master
```
roscore
```
打开海龟仿真器
```
rosrun turtlesim turtlesim_node
```
启动publisher
```
rosrun learning velocity_publisher.py
```
启动Subscriber
```
rosrun learning pose_subscriber.py
```
即可看到海龟的实时坐标
### 自定义话题消息
##### 消息定义
在功能包文件夹内创建msg文件夹，并新建Person.msg文件，在里面写入
```
string name
uint8  age
uint8  sex

uint8 unknown = 0
uint8 male    = 1
uint8 female  = 2
```
##### 添加依赖
在`package.xml`文件内添加依赖：
```
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
```
在`CMakeLists.txt`内加入：
```
add_message_files(
  FILES
  Person.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)
```
并把
```
#  CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs turtlesim
```
改为
```
   CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs turtlesim message_runtime
```
##### 实验程序
在功能包`scripts`文件夹内创建：
person_publisher.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

import rospy
from learning.msg import Person

def velocity_publisher():
	# ROS节点初始化
    rospy.init_node('person_publisher', anonymous=True)

	# 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10
    person_info_pub = rospy.Publisher('/person_info', Person, queue_size=10)

	#设置循环的频率
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
		# 初始化learning_topic::Person类型的消息
    	person_msg = Person()
    	person_msg.name = "Tom";
    	person_msg.age  = 18;
    	person_msg.sex  = Person.male;

		# 发布消息
        person_info_pub.publish(person_msg)
    	rospy.loginfo("Publsh person message[%s, %d, %d]", 
				person_msg.name, person_msg.age, person_msg.sex)

		# 按照循环频率延时
        rate.sleep()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
```
person_subscriber.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将订阅/person_info话题，自定义消息类型learning_topic::Person

import rospy
from learning.msg import Person

def personInfoCallback(msg):
    rospy.loginfo("Subcribe Person Info: name:%s  age:%d  sex:%d", 
			 msg.name, msg.age, msg.sex)

def person_subscriber():
	# ROS节点初始化
    rospy.init_node('person_subscriber', anonymous=True)

	# 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/person_info", Person, personInfoCallback)

	# 循环等待回调函数
    rospy.spin()

if __name__ == '__main__':
    person_subscriber()
```
分别启动后即可看见收发的文件
## 服务：服务端与客户端
### Client
##### 功能包代码
person_client.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/show_person服务，服务数据类型learning_service::Person

import sys
import rospy
from learning_service.srv import Person, PersonRequest

def person_client():
	# ROS节点初始化
    rospy.init_node('person_client')

	# 发现/spawn服务后，创建一个服务客户端，连接名为/spawn的service
    rospy.wait_for_service('/show_person')
    try:
        person_client = rospy.ServiceProxy('/show_person', Person)

		# 请求服务调用，输入请求数据
        response = person_client("Tom", 20, PersonRequest.male)
        return response.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
	#服务调用并显示调用结果
    print "Show person result : %s" %(person_client())
```
##### 执行
1.打开ros master
```
roscore
```
2.启动海龟仿真器
```
rosrun turtlesim turtlesim_node
```
3.启动程序
```
rosrun learning turtle_spawn.py
```
即可看到产生了一个新的海龟

### Server
##### 功能包代码
person_server.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将执行/show_person服务，服务数据类型learning_service::Person

import rospy
from learning_service.srv import Person, PersonResponse

def personCallback(req):
	# 显示请求数据
    rospy.loginfo("Person: name:%s  age:%d  sex:%d", req.name, req.age, req.sex)

	# 反馈数据
    return PersonResponse("OK")

def person_server():
	# ROS节点初始化
    rospy.init_node('person_server')

	# 创建一个名为/show_person的server，注册回调函数personCallback
    s = rospy.Service('/show_person', Person, personCallback)

	# 循环等待回调函数
    print "Ready to show person informtion."
    rospy.spin()

if __name__ == "__main__":
    person_server()
```
##### 执行
1.打开ros master
```
roscore
```
2.启动海龟仿真器
```
rosrun turtlesim turtlesim_node
```
3.启动程序
```
rosrun learning turtle_command_server.py
```
4.发布信息
```
rosservice call /turtle_command "{}"
```
发送即可看到海龟开始运动，再次发布即停止
##### 查看服务数据定义
```
rossrv show <服务>
```
返回内容`---`之上为request，之下为responce
### 自定义服务数据
##### 服务数据定义
新建srv文件夹并写入Person.srv
```
string name
uint8  age
uint8  sex

uint8 unknown = 0
uint8 male    = 1
uint8 female  = 2

---
string result
```
##### 添加依赖
在`package.xml`添加：
```
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
```
在`CMakeList.txt`添加：
```
add_service_files(
  FILES
  Person.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)
```
##### 实验程序
person_server.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将执行/show_person服务，服务数据类型learning_service::Person

import rospy
from learning.srv import Person, PersonResponse

def personCallback(req):
	# 显示请求数据
    rospy.loginfo("Person: name:%s  age:%d  sex:%d", req.name, req.age, req.sex)

	# 反馈数据
    return PersonResponse("OK")

def person_server():
	# ROS节点初始化
    rospy.init_node('person_server')

	# 创建一个名为/show_person的server，注册回调函数personCallback
    s = rospy.Service('/show_person', Person, personCallback)

	# 循环等待回调函数
    print "Ready to show person informtion."
    rospy.spin()

if __name__ == "__main__":
    person_server()
```
person_client.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/show_person服务，服务数据类型learning_service::Person

import sys
import rospy
from learning.srv import Person, PersonRequest

def person_client():
	# ROS节点初始化
    rospy.init_node('person_client')

	# 发现/spawn服务后，创建一个服务客户端，连接名为/spawn的service
    rospy.wait_for_service('/show_person')
    try:
        person_client = rospy.ServiceProxy('/show_person', Person)

		# 请求服务调用，输入请求数据
        response = person_client("Tom", 20, PersonRequest.male)
        return response.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
	#服务调用并显示调用结果
    print "Show person result : %s" %(person_client())
```
##### 执行
1.ros master
```
roscore
```
2.服务端
```
rosrun learning person_server.py
```
3.客户端
```
rosrun learning person_client.py
```
即可看到客户端与服务端相互通信

## 参数：全局字典
### 命令行的使用
1.列出参数
```
rosparam list
```
2.获取参数值
```
rosparam get <参数>
```
3.修改参数
```
rosparam set <参数>
```
4.保存参数为文件
```
rosparam dump xxx.yaml
```
5.从文件加载参数
```
rosparam load xxx.yaml
```
6.删除参数
```
rosparam delete xxx.yaml
```
### 用python程序对参数操作
parameter_config.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程设置/读取海龟例程中的参数

import sys
import rospy
from std_srvs.srv import Empty

def parameter_config():
	# ROS节点初始化
    rospy.init_node('parameter_config', anonymous=True)

	# 读取背景颜色参数
    red   = rospy.get_param('/turtlesim/background_r')
    green = rospy.get_param('/turtlesim/background_g')
    blue  = rospy.get_param('/turtlesim/background_b')

    rospy.loginfo("Get Backgroud Color[%d, %d, %d]", red, green, blue)

	# 设置背景颜色参数
    rospy.set_param("/turtlesim/background_r", 255);
    rospy.set_param("/turtlesim/background_g", 255);
    rospy.set_param("/turtlesim/background_b", 255);

    rospy.loginfo("Set Backgroud Color[255, 255, 255]");

	# 读取背景颜色参数
    red   = rospy.get_param('/turtlesim/background_r')
    green = rospy.get_param('/turtlesim/background_g')
    blue  = rospy.get_param('/turtlesim/background_b')

    rospy.loginfo("Get Backgroud Color[%d, %d, %d]", red, green, blue)

	# 发现/spawn服务后，创建一个服务客户端，连接名为/spawn的service
    rospy.wait_for_service('/clear')
    try:
        clear_background = rospy.ServiceProxy('/clear', Empty)

		# 请求服务调用，输入请求数据
        response = clear_background()
        return response
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    parameter_config()
```
## launch
### 文件语法
##### 根元素
用`<launch>`标签定义
以`</launch>`结尾
##### 启动节点
`<node pkg="package_name" name="executable_name" name="node_name" />`
pkg:节点所在功能包名称
type:可执行文件名称
name:节点运行时名称
output,respawn,......参数
##### 添加参数
`<param name="output_frame value="pdom" />`
name:参数名
value:参数值
还有`<ary>`添加参数，仅供launch内部使用
##### 重映射（重命名）
`<remap from="/a/b" to="/c" />`
from:原名称
to:映射后的命名
##### 嵌套
包含其他launch文件
`<include file="path">`
file:其他launch文件路径
### 实例
1.

```xml
<launch>
    <node pkg="learning_topic" type="person_subscriber" name="talker" output="screen" />
    <node pkg="learning_topic" type="person_publisher" name="listener" output="screen" /> 
</launch>
```
2.

```xml
<launch>

	<!-- Turtlesim Node-->
	<node pkg="turtlesim" type="turtlesim_node" name="sim"/>
	<node pkg="turtlesim" type="turtle_teleop_key" name="teleop" output="screen"/>

	<node name="turtle1_tf_broadcaster" pkg="learning_tf" type="turtle_tf_broadcaster.py">
	  <param name="turtle" type="string" value="turtle1" />
	</node>
	<node name="turtle2_tf_broadcaster" pkg="learning_tf" type="turtle_tf_broadcaster.py">
	  <param name="turtle" type="string" value="turtle2" /> 
	</node>

    <node pkg="learning_tf" type="turtle_tf_listener.py" name="listener" />

</launch>
```
3.

```xml
<launch>

	<param name="/turtle_number"   value="2"/>

    <node pkg="turtlesim" type="turtlesim_node" name="turtlesim_node">
		<param name="turtle_name1"   value="Tom"/>
		<param name="turtle_name2"   value="Jerry"/>

		<rosparam file="$(find learning_launch)/config/param.yaml" command="load"/>
	</node>

    <node pkg="turtlesim" type="turtle_teleop_key" name="turtle_teleop_key" output="screen"/>

</launch>
```
4.

```xml
<launch>

	<include file="$(find learning_launch)/launch/simple.launch" />

    <node pkg="turtlesim" type="turtlesim_node" name="turtlesim_node">
		<remap from="/turtle1/cmd_vel" to="/cmd_vel"/>
	</node>

</launch>
```
## ROS命令行工具
### ROS Master
##### 1.启动ROS Master
```
roscore
```
### 信息查询
##### 2.可视化查看节点关系
```
rqt_graph
```
##### 3.查看节点信息`rosnode`
```
#查看全部节点
rosnode list

#查看节点详细信息
rosnode info <节点名>

#......
```
##### 4.查看话题`rostopic`
```
#打印话题列表
rostopic list

#给话题发布数据
rostopic pub <话题名> <数据内容>
##数据内容可用两次tab补全默认格式
##可加参数 -r <频率(Hz)> 来连续发布

#......
```
##### 5.查看消息`rosmsg`
```
#查看消息数据结构
rosmsg show <话题名>

#......
```
##### 6.查看服务`rosservice`
```
#查看所有服务
rosservice list

#发布服务请求
rosservice call <服务名>

#......
```
### 信息记录
##### 7.记录工具
```
#记录话题数据
rosbag record -a -O <压缩数据包名>
##其中-a表示all保存全部数据，-O表示保存成压缩包

#复现话题数据
rosbag paly <复现文件名>
```

## 常用工具
### rqt
日志输出工具`rqt_console`
计算图可视化工具`rqt_graph`
数据绘图工具`rqt_plot`
图像渲染工具`rqt_image_view`
### rviz,gazebo
emmm可能以后再讲吧