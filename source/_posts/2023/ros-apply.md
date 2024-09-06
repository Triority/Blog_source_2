---
title: ros实操记录
tags:
  - 笔记
  - linux
  - python
  - ROS
cover: /img/ros.png
categories:
- [文档&笔记]
- [折腾记录]
- [值得一提的文章]
date: 2023-06-05 00:11:24
description: 这部分文章是从最基础那篇文章分离出来的，不然那个太长了hhh
---
# 前言
这篇文章是从最基础那篇文章分离出来的，不然那个太长了找起东西太麻烦

同时也部分记录2023年的人工智能竞赛学习开发过程
# 前置任务(在比赛的车上获取传感器信息)
这一部分除了比赛那辆车以外都用不到，也就不详细分目录了，不想占用目录太多空间

> IMU

首先查看一下IMU的地址
```sh
ros-autocar@ros-autocar:~$ ls /dev/ttyUSB*
/dev/ttyUSB1  /dev/ttyUSB2  /dev/ttyUSB3
ros-autocar@ros-autocar:~$ ls /dev/ttyUSB*
/dev/ttyUSB0  /dev/ttyUSB1  /dev/ttyUSB2  /dev/ttyUSB3
```
有四个设备，拔掉imu之后再次查看少了那个就知道imu的地址了。给IMU的设备添加读写权限：
```sh
sudo chmod  +777 /dev/ttyUSB0
```
然后使用资料给的命令就可以读取imu的数值了
```sh
roslaunch imu_launch  imu_msg.launch
```
```sh
header: 
  seq: 18691
  stamp: 
    secs: 1685621438
    nsecs: 130887727
  frame_id: "base_link"
orientation: 
  x: 0.03581126779317856
  y: -0.006689701694995165
  z: -0.002406603889539838
  w: 0.999333381652832
orientation_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
angular_velocity: 
  x: 5.624821674786508e-05
  y: -0.0020166519167128206
  z: -0.001579628805375099
angular_velocity_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
linear_acceleration: 
  x: 0.19336825460195542
  y: 0.6750088781118393
  z: 9.727661895751954
linear_acceleration_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
---
```

***

> 激光雷达

资料给了驱动雷达的功能包，启动雷达的launch命令：
这个launch文件有一个地方需要改动就是雷达串口设备号，我这一次改成是`/dev/ttyUSB2`如果启动文件之后雷达不转可以考虑是这个问题
```sh
roslaunch ls01b_v2 ls01b_v2.launch
```
然后在另外一个终端查看雷达数据：应该会看到满屏的数字hhh都是雷达扫描到的距离信息
```sh
rostopic echo /scan
```

***

> 编码器

同样，使用资料的驱动功能包：

```sh
roscore
rosrun encoder_driver Encoder_vel.py
rostopic echo /encoder
```
输出：
```sh
header: 
  seq: 11316
  stamp: 
    secs: 1685623435
    nsecs: 710257768
  frame_id: "odom"
child_frame_id: "base_footprint"
pose: 
  pose: 
    position: 
      x: 0.0
      y: 0.0
      z: 0.0
    orientation: 
      x: 0.0
      y: 0.0
      z: 0.0
      w: 0.0
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
twist: 
  twist: 
    linear: 
      x: 0.05552978515624999
      y: 0.0
      z: 0.0
    angular: 
      x: 0.0
      y: 0.0
      z: 0.0
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
---
```
其中`x: 0.05552978515624999`表示前进速度

***

> 整合及运动控制

```sh
roslaunch racecar Run_car.launch 
rosrun racecar racecar_teleop.py
rviz rviz
```
第一个启动了上述传感器的程序：
![](微信截图_20230605212637.png)
第二个用于使用键盘发布信息控制底盘，最后是rviz用于显示雷达等信息。

其中雷达需要设置坐标变换，雷达的坐标是相对于底盘坐标定义的，rviz默认使用map坐标系显示，需要定义底盘坐标系和map坐标系的相对关系。
```xml
<node pkg="tf" type="static_transform_publisher" name="map_odom_broadcaster" args="0 0 0 0 0 0 /map /odom 100" />

```
其实临时也可以把rviz的frame改为雷达坐标系解决。

# 常用算法
## 激光里程计：rf2o_laser_odometry
这个功能包可以根据激光雷达两帧之间的位置差距计算车子实际走的距离。

[github链接](https://github.com/MAPIRlab/rf2o_laser_odometry)

下载的功能包放在src文件夹内，需要做一些配置和修改一些bug：

首先是修改launch文件的话题节点等名称，这里我是改成这样

`rf2o_laser_odometry.launch`
```xml
<launch>
 
  <node pkg="rf2o_laser_odometry" type="rf2o_laser_odometry_node" name="rf2o_laser_odometry" output="screen">
    <param name="laser_scan_topic" value="/scan"/>        # 雷达发布数据的话题
    <param name="odom_topic" value="/odom" />             # 发布测程估计的topic
    <param name="publish_tf" value="true" />              # 是否发布tf变换(base->odom)
    <param name="base_frame_id" value="/base_footprint"/> # 底盘的frame_id (tf) 必须要雷达laser_frame到base_frame的tf变换
    <param name="odom_frame_id" value="/odom" />          # 发布测程估计的frame_id (tf) 
    <param name="init_pose_from_topic" value="" />        # Odom 话题初始点，留空从(0,0)开始
    <param name="freq" value="10.0"/>                     # 执行频率
    <param name="verbose" value="true"/>                  # verbose
  </node>
</launch>
```

接下来改一些bug：修改`src/CLaserOdometry2D.cpp`

292-298行修改:
```cpp
//Inner pixels
if ((u>1)&&(u<cols_i-2))
{
if (dcenter > 0.f)
if (std::isfinite(dcenter) && dcenter > 0.f)
{
float sum = 0.f;
float weight = 0.f;

```
316-322行修改:
```cpp
//Boundary
else
{
if (dcenter > 0.f)
if (std::isfinite(dcenter) && dcenter > 0.f)
{
float sum = 0.f;
float weight = 0.f;

```

打开底盘lanunch文件，并启动rf2o：
```sh
roslaunch rf2o_laser_odometry rf2o_laser_odometry.launch 
```
就可以看见终端输出的里程数据。这个方法得到的数据有些缺陷，就是在车子发生旋转时候是不准确的，因为雷达和车子都在旋转相对位置不准确。

![](rf2o.png)

还有一个bug，如果你把车子往前推，结果rf2o输出为负方向，那么需要改一下代码：
`CLaserOdometry2D.cpp`：
```
Line 923:
  pose_aux_2D.translation()(0) = -acu_trans(0,2);
  pose_aux_2D.translation()(1) = -acu_trans(1,2);
Line 956:
  lin_speed = -acu_trans(0,2) / time_inc_sec;
```
## 使用编码器和imu定位
这段代码是志伟学长写的，我就一边学习理解一边写写注释吧
```python
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from scipy.spatial.transform import Rotation
import numpy as np
import time
import tf2_ros
from geometry_msgs.msg import Pose, Point, Quaternion, TransformStamped, PoseArray
import tf_conversions
import message_filters
from math import sin, cos, pi,sqrt,fabs

last_angle = None
last_vel = None
last_time = None
pos_x = 0
pos_y = 0
br = tf2_ros.TransformBroadcaster()
encoder_dx = 27.7/1000.0

def callback(imu_data, encoder_data):
    global last_angle, last_vel, last_time, pos_x, pos_y
    # 获取imu数据
    r = Rotation.from_quat([imu_data.orientation.x, 
                            imu_data.orientation.y, 
                            imu_data.orientation.z, 
                            imu_data.orientation.w])
    angle = r.as_euler('xyz')[2]
    if angle<0:
        angle = 2*np.pi + angle
    # 忽略错误数据
    if encoder_data.twist.twist.linear.x>10 or encoder_data.twist.twist.linear.x<-10:
        return
    
    if last_time is None:
        last_time = encoder_data.header.stamp
        last_angle = angle
        last_vel = encoder_data.twist.twist.linear.x
        return
    # 位置计算
    dt = (encoder_data.header.stamp - last_time).to_sec()
    last_time = encoder_data.header.stamp


    d = (encoder_data.twist.twist.linear.x+last_vel)/2.0*dt
    last_vel = encoder_data.twist.twist.linear.x

    d_angle = np.fabs(angle - last_angle)
    if angle - last_angle>0.00001:
        l = d / d_angle+encoder_dx
        d = l * np.sqrt(2*(1-np.cos(d_angle)))
    elif angle - last_angle<-0.00001:
        l = d / d_angle-encoder_dx
        d = l * np.sqrt(2*(1-np.cos(d_angle)))
    
    last_angle = angle
    
    d_x = d * np.cos(angle)
    d_y = d * np.sin(angle)
    pos_x += d_x
    pos_y += d_y
    # 发布位置坐标变换信息
    t = TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "odom"
    t.child_frame_id = "base_link"
    t.transform.translation.x = pos_x
    t.transform.translation.y = pos_y
    t.transform.translation.z = 0.0

    q = tf_conversions.transformations.quaternion_from_euler(0, 0, angle)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    br.sendTransform(t)
    odom_data = Odometry()
    odom_data.header.stamp = rospy.Time.now()
    odom_data.header.frame_id = "odom"
    odom_data.child_frame_id = "base_link"
    odom_data.pose.pose.position.x = pos_x
    odom_data.pose.pose.position.y = pos_y
    odom_data.pose.pose.position.z = 0.0
    odom_data.pose.pose.orientation.x = q[0]
    odom_data.pose.pose.orientation.y = q[1]
    odom_data.pose.pose.orientation.z = q[2]
    odom_data.pose.pose.orientation.w = q[3]
    odom_pub.publish(odom_data)
    
# 初始化encoder_mix节点
rospy.init_node('encoder_mix')
# 创建Subscriber，订阅imu和编码器的topic
imu_sub = message_filters.Subscriber('/imu_data', Imu)
encoder_sub = message_filters.Subscriber('/encoder', Odometry)
# 使用自适应算法来匹配基于其时间戳的消息并执行回调函数，详见https://blog.csdn.net/chishuideyu/article/details/77479758
ts = message_filters.ApproximateTimeSynchronizer([imu_sub, encoder_sub], 20, 0.1)
ts.registerCallback(callback)
# 
odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
rospy.spin()
```


## 传感器数据融合：robot localization/ekf



## 激光雷达建图：gmapping/cartographer
[gmapping的github](https://github.com/ros-perception/slam_gmapping)

gmapping安装：
```
sudo apt-get install ros-noetic-slam-gmapping
```
编写一个新的launch文件：
```xml
<launch>
    <arg name="scan_topic" default="scan" />                  <!-- 发布scan名称 -->
    <node pkg="gmapping" type="slam_gmapping" name="slam_gmapping" output="screen" clear_params="true">
        <param name="base_frame" value="base_link"/>     <!-- 基座标系名称 -->
        <param name="odom_frame" value="odom"/>               <!-- 里程计坐标系名称 -->
        <param name="map_update_interval" value="4.0"/>
        <!-- Set maxUrange < actual maximum range of the Laser -->
        <param name="maxRange" value="5.0"/>
        <param name="maxUrange" value="4.5"/>
        <param name="sigma" value="0.05"/>
        <param name="kernelSize" value="1"/>
        <param name="lstep" value="0.05"/>
        <param name="astep" value="0.05"/>
        <param name="iterations" value="5"/>
        <param name="lsigma" value="0.075"/>
        <param name="ogain" value="3.0"/>
        <param name="lskip" value="0"/>
        <param name="srr" value="0.01"/>
        <param name="srt" value="0.02"/>
        <param name="str" value="0.01"/>
        <param name="stt" value="0.02"/>
        <param name="linearUpdate" value="0.5"/>
        <param name="angularUpdate" value="0.436"/>
        <param name="temporalUpdate" value="-1.0"/>
        <param name="resampleThreshold" value="0.5"/>
        <param name="particles" value="80"/>
        <param name="xmin" value="-1.0"/>
        <param name="ymin" value="-1.0"/>
        <param name="xmax" value="1.0"/>
        <param name="ymax" value="1.0"/>
        <param name="delta" value="0.05"/>
        <param name="llsamplerange" value="0.01"/>
        <param name="llsamplestep" value="0.01"/>
        <param name="lasamplerange" value="0.005"/>
        <param name="lasamplestep" value="0.005"/>
        <remap from="scan" to="$(arg scan_topic)"/>
    </node>
</launch>
```
启动launch文件：
```sh
roslaunch test gmapping.launch
```
![](gmapping.png)

建图后，在想要保存的路径打开终端并输入使用mapserver保存命令：
```sh
ros-autocar@ros-autocar:~/Ros-autocar$ rosrun map_server map_saver -f 233
[ INFO] [1685971241.710265601]: Waiting for the map
[ INFO] [1685971241.931482169]: Received a 480 X 544 map @ 0.050 m/pix
[ INFO] [1685971241.931548164]: Writing map occupancy data to 233.pgm
[ INFO] [1685971241.942866551]: Writing map occupancy data to 233.yaml
[ INFO] [1685971241.943307197]: Done
```
`233`为保存地图的文件名

补充一个launch文件启动rviz的代码：
```xml
    <!-- rviz -->
    <node pkg="rviz" type="rviz" name="rviz" args="-d /home/ros-autocar/Ros-autocar/rviz.rviz" required="true" />
```
其中`/home/ros-autocar/Ros-autocar/rviz.rviz`是rviz配置文件的路径

## 读取建立的地图：map_server
只要把这一段放在启动rviz的launch文件里就好啦
```xml
<node pkg="map_server" type="map_server" name="map_server" args="/home/ros-autocar/Ros-manualcar/map.yaml"/>
```
`args`要改成你的地图的路径

## 重定位：amcl
与rf2o的雷达两帧之间比较不同，amcl是根据雷达数据和地图之间比较计算里程计误差，也就是计算/odom和/map之间的坐标变换关系

在launch文件加入这一大部分即可启动amcl
```xml
<!-- amcl -->
    <arg name="init_x" default="0" />
    <arg name="init_y" default="0" />
    <arg name="init_a" default="0" />
    <node pkg="amcl" type="amcl" name="amcl" output="screen">
        <!-- Publish scans from best pose at a max of 10 Hz -->
        <param name="transform_tolerance" value="0.2" />
        <param name="gui_publish_rate" value="10.0"/>
        <param name="laser_max_beams" value="30"/>
        <param name="min_particles" value="100"/>
        <param name="max_particles" value="5000"/>
        <param name="kld_err" value="0.01"/>
        <param name="kld_z" value="0.99"/>
        <!-- translation std dev, m -->
        <param name="odom_alpha1" value="0.2"/>
        <param name="odom_alpha2" value="0.2"/>
        <param name="odom_alpha3" value="0.8"/>
        <param name="odom_alpha4" value="0.2"/>
        <param name="laser_z_hit" value="0.5"/>
        <param name="laser_z_short" value="0.05"/>
        <param name="laser_z_max" value="0.05"/>
        <param name="laser_z_rand" value="0.5"/>
        <param name="laser_sigma_hit" value="0.2"/>
        <param name="laser_lambda_short" value="0.1"/>
        <param name="laser_lambda_short" value="0.1"/>
        <param name="laser_model_type" value="likelihood_field"/>

        <!-- <param name="laser_model_type" value="beam"/> -->
        <param name="laser_likelihood_max_dist" value="2.0"/>
        <param name="update_min_d" value="0.1"/>
        <param name="update_min_a" value="0.1"/>
        <param name="resample_interval" value="2"/>
        <param name="transform_tolerance" value="0.1"/>
        <param name="recovery_alpha_slow" value="0.0"/>
        <param name="recovery_alpha_fast" value="0.1"/>

        <param name="use_map_topic" value="true"/>
        <param name="first_map_only" value="true"/>
        <param name="tf_broadcast" value="true"/>

        <param name="odom_frame_id" value="odom"/>
        <param name="global_frame_id" value="map"/>
        <param name="base_frame_id" value="base_link"/>
        <param name="odom_model_type" value="diff"/>

        <param name="initial_pose_x" value="$(arg init_x)"/>
        <param name="initial_pose_y" value="$(arg init_y)"/>
        <param name="initial_pose_a" value="$(arg init_a)"/>
        <param name="initial_cov_xx" value="0.25" />
        <param name="initial_cov_yy" value="0.25" />
        <param name="initial_cov_aa" value="0.5" />
    </node>
```
里面有很多的参数，如果需要调试在[amcl的网页](http://wiki.ros.org/amcl)有详细信息

## 路径规划：全局/局部
### 全局：A*

具体原理文章太多了直接去搜吧，不想写了，至于导航的实操详见下面局部路径规划

### 局部：DWA，teb
#### 动态窗口法：DWA
> 全称为`dynamic window approach`，其原理主要是在速度空间（v,w）中采样多组速度，并模拟出这些速度在一定时间内的运动轨迹，并通过评价函数对这些轨迹进行评价，选取最优轨迹对应的速度驱动机器人运动

优缺点：考虑到速度和加速度的限制只有安全的轨迹会被考虑；可以实时避障但是避障效果一般；不适用于阿克曼模型车模；每次都选择下一步的最佳路径而非全局最优路径

这个可能暂时先不写，因为我现在实验用的车子是阿克曼结构hhh

#### 时间弹性带：teb
> 全称为`Time Elastic Band`，连接起始、目标点，并让这个路径可以变形，变形的条件就是将所有约束当做橡皮筋的外力。起始点、目标点状态由用户/全局规划器指定，中间插入N个控制橡皮筋形状的控制点（机器人姿态），当然，为了显示轨迹的运动学信息，我们在点与点之间定义运动时间Time，即为`Timed-Elastic-Band`算法

优缺点：适用于各种常见车模；有很强的前瞻性；对动态障碍有较好的避障效果；计算复杂度较大但是可通过牺牲预测距离来降低；速度和角度波动较大控制不稳定但是提高控制频率可以改善

首先下载功能包然后`catkin_make`
```sh
git clone https://github.com/rst-tu-dortmund/teb_local_planner
```
查看是否安装完成，找到`teb_local_planner`的话就表示安装成功了：
```sh
rospack plugins --attrib=plugin nav_core
```
![我也不觉得这张图有什么必要，但是突然就是想放一张图hhh](QQ截图20230608143529.png)

看见有一个包含teb_local_planner教程补充材料和示例的项目[teb_local_planner_tutorials](https://github.com/rst-tu-dortmund/teb_local_planner_tutorials)，我的是阿克曼结构车子，参考里面的`robot_carlike_in_stage.launch`，其中里面有一部分我们已经在之前完成了，例如amcl等，所以用得到的地方就是这一段(加入了launch标签)：
```xml
<launch>
<!--  ************** Navigation ***************  -->
	<node pkg="move_base" type="move_base" respawn="false" name="move_base" output="screen">
  	  	<rosparam file="$(find teb_local_planner_tutorials)/cfg/carlike/costmap_common_params.yaml" command="load" ns="global_costmap" />
  	 	<rosparam file="$(find teb_local_planner_tutorials)/cfg/carlike/costmap_common_params.yaml" command="load" ns="local_costmap" />
  		<rosparam file="$(find teb_local_planner_tutorials)/cfg/carlike/local_costmap_params.yaml" command="load" />
  		<rosparam file="$(find teb_local_planner_tutorials)/cfg/carlike/global_costmap_params.yaml" command="load" />
  		<rosparam file="$(find teb_local_planner_tutorials)/cfg/carlike/teb_local_planner_params.yaml" command="load" />

		<param name="base_global_planner" value="global_planner/GlobalPlanner" />
		<param name="planner_frequency" value="1.0" />
		<param name="planner_patience" value="5.0" />

		<param name="base_local_planner" value="teb_local_planner/TebLocalPlannerROS" />
		<param name="controller_frequency" value="5.0" />
		<param name="controller_patience" value="15.0" />

                <param name="clearing_rotation_allowed" value="false" /> <!-- Our carlike robot is not able to rotate in place -->
	</node>
</launch>
```

启动之前的launch文件和这一部分之后就能看见规划的路径了：
![The Green Path](微信截图_20230608180121.png)

launch文件里也给出了几个配置文件的路径，包括代价地图的配置，路径规划器的参数配置，这个后面再说

路线规划之后就是让车子跟着规划走下来了，我刚准备手搓一个程序，发现示例代码给了...

示例的launch文件导航相关片段：
```xml
    <!-- Navstack -->
    <node pkg="move_base" type="move_base" respawn="false" name="move_base">
        <!-- local planner -->
      
        <param name="base_global_planner" value="navfn/NavfnROS"/>  
        <param name="base_local_planner" value="dwa_local_planner/DWAPlannerROS"/>  
        <rosparam file="$(find racecar)/param/dwa_local_planner_params.yaml" command="load"/>
        
        <!-- costmap layers -->    
        <rosparam file="$(find racecar)/param/local_costmap_params.yaml" command="load"/>
        <rosparam file="$(find racecar)/param/global_costmap_params.yaml" command="load"/> 
        <!-- move_base params -->
        <rosparam file="$(find racecar)/param/base_global_planner_params.yaml" command="load"/>
        <rosparam file="$(find racecar)/param/move_base_params.yaml" command="load"/>
    </node>

    <node pkg="racecar" type="car_controller_new" respawn="false" name="car_controller" output="screen">       
       
        <param name="Vcmd" value="1.5" /> <!--speed of car m/s         -->
        <!-- ESC -->
        <param name="baseSpeed" value="150"/> 
        <param name="baseAngle" value="0.0"/> 
        <param name="Angle_gain_p" value="-3.0"/> 
        <param name="Angle_gain_d" value="-3.0"/> 
        <param name="Lfw" value="1.5"/> 
        <param name="vp_max_base" value="200"/> 
        <param name="vp_min" value="200"/> 

    </node>
```
`car_controller_new.cpp`这个程序好长的，建议不要打开hhhhc反正我肯定是重写一个：
```cpp
#include "nav_msgs/Path.h"
#include "ros/ros.h"
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Twist.h>
#include <iostream>
#include <nav_msgs/Odometry.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>
#include <visualization_msgs/Marker.h>
#include <dynamic_reconfigure/server.h>

#include <cmath>
#include <std_msgs/Float64.h>

#define PI 3.14159265358979
double last_steeringangle = 0;
double L, Lfw, Lrv, Lfw_, Vcmd, lfw, lrv, steering, u, v;
double Gas_gain, baseAngle, baseSpeed, Angle_gain_p, Angle_gain_d, goalRadius;
int controller_freq;
bool foundForwardPt, goal_received, goal_reached;
double k_rou;
double vp_max_base, vp_min;
double stop_flag = 0.0;
int mapPathNum;
double slow_final, fast_final;
int stopIdx = 0;
double line_wight = 0.0;
double initbaseSpeed;
double obs_flag = 0.0;

/********************/
/* CLASS DEFINITION */
/********************/
class L1Controller
{
public:
  L1Controller();
  void initMarker();
  bool isWayPtAwayFromLfwDist(const geometry_msgs::Point &wayPt, const geometry_msgs::Point &car_pos);
  bool isForwardWayPt(const geometry_msgs::Point &wayPt, const geometry_msgs::Pose &carPose);
  double getYawFromPose(const geometry_msgs::Pose &carPose);
  double getEta(const geometry_msgs::Pose &carPose);
  double getCar2GoalDist();
  double getL1Distance(const double &_Vcmd);
  double getSteeringAngle(double eta);
  double getGasInput(const float &current_v);
  double isline(double line_wight);
  geometry_msgs::Point get_odom_car2WayPtVec(const geometry_msgs::Pose &carPose);

private:
  ros::NodeHandle n_;
  ros::Subscriber odom_sub, path_sub, goal_sub, encoder_sub, final_goal_sub, line_sub;
  ros::Publisher pub_, marker_pub;
  ros::Timer timer1, timer2;
  tf::TransformListener tf_listener;

  visualization_msgs::Marker points, line_strip, goal_circle;
  geometry_msgs::Twist cmd_vel;
  geometry_msgs::Point odom_goal_pos;
  nav_msgs::Odometry odom, encoder;
  nav_msgs::Path map_path, odom_path;

  void odomCB(const nav_msgs::Odometry::ConstPtr &odomMsg);
  void pathCB(const nav_msgs::Path::ConstPtr &pathMsg);
  void encoderCB(const nav_msgs::Odometry::ConstPtr &encoderMsg);
  void goalCB(const geometry_msgs::PoseStamped::ConstPtr &goalMsg);
  void goalReachingCB(const ros::TimerEvent &);
  void controlLoopCB(const ros::TimerEvent &);
  void stopCB(const std_msgs::Float64::ConstPtr &stopMsg);
  void lineCB(const std_msgs::Float64::ConstPtr &lineMsg);

}; // end of class

L1Controller::L1Controller()
{
  // Private parameters handler
  ros::NodeHandle pn("~");

  // Car parameter
  pn.param("L", L, 0.335);      //前后轮轴距
  pn.param("Vcmd", Vcmd, 1.0);  //期望速度
  pn.param("lfw", lfw, 0.1675); //车身转向控制点
  pn.param("lrv", lrv, 10.0);   //车身转向控制点
  pn.param("Lrv", Lrv, 10.0);

  // Controller parameter
  pn.param("controller_freq", controller_freq, 30); //控制循环频率
  pn.param("Angle_gain_p", Angle_gain_p, -1.0);
  pn.param("Angle_gain_d", Angle_gain_d, -0.0);
  pn.param("baseSpeed", baseSpeed, 0.0); //基础速度
  pn.param("baseAngle", baseAngle, 0.0); //舵机中值     舵机打角steeringangle设为-90度～90度
  pn.param("k_rou", k_rou, 0.0);         //类曲率调速的系数
  pn.param("vp_max_base", vp_max_base, 0.0);
  pn.param("vp_min", vp_min, 0.0);
  pn.param("goalRadius", goalRadius, 1.0);
  pn.param("Lfw", Lfw, 0.3);
  pn.param("slow_final", slow_final, 0.8);
  pn.param("fast_final", fast_final, 1.1);
  initbaseSpeed = baseSpeed;
  odom_sub = n_.subscribe("/odometry/filtered", 1, &L1Controller::odomCB, this); //订阅里程计
  path_sub = n_.subscribe("/move_base/NavfnROS/plan", 1, &L1Controller::pathCB, this);
  goal_sub = n_.subscribe("/move_base_simple/goal", 1, &L1Controller::goalCB, this); //订阅movebase目标点
  encoder_sub = n_.subscribe("/encoder", 1, &L1Controller::encoderCB, this);         //订阅编码器
  final_goal_sub = n_.subscribe("/arrfinal", 1, &L1Controller::stopCB, this);
  line_sub = n_.subscribe("/line_wight", 1, &L1Controller::lineCB, this);
  marker_pub = n_.advertise<visualization_msgs::Marker>("car_path", 10); //发布路径到rviz
  pub_ = n_.advertise<geometry_msgs::Twist>("car/cmd_vel", 1);           //发布速度、角速度

  // Timer
  timer1 = n_.createTimer(ros::Duration((1.0) / controller_freq), &L1Controller::controlLoopCB, this);  // Duration(0.05) -> 20Hz
  timer2 = n_.createTimer(ros::Duration((0.5) / controller_freq), &L1Controller::goalReachingCB, this); // Duration(0.05) -> 20Hz

  // 初始化变量
  //Lfw = 1.1; //前瞻
  foundForwardPt = false;
  goal_received = false;
  goal_reached = false;
  cmd_vel.linear.x = 0;          // 0 for stop
  cmd_vel.angular.z = baseAngle; //中值

  // Show info
  ROS_INFO("[param] baseSpeed: %f", baseSpeed);
  ROS_INFO("[param] baseAngle: %f", baseAngle);
  ROS_INFO("[param] Angle_gain_p: %f", Angle_gain_p);
  ROS_INFO("[param] Angle_gain_d: %f", Angle_gain_d);
  ROS_INFO("[param] Vcmd: %f", Vcmd);
  ROS_INFO("[param] Lfw: %f", Lfw);

  // Visualization Marker Settings
  initMarker();
}

//rviz可视化初始化
void L1Controller::initMarker()
{
  points.header.frame_id = line_strip.header.frame_id = goal_circle.header.frame_id = "odom";
  points.ns = line_strip.ns = goal_circle.ns = "Markers";
  points.action = line_strip.action = goal_circle.action = visualization_msgs::Marker::ADD;
  points.pose.orientation.w = line_strip.pose.orientation.w = goal_circle.pose.orientation.w = 1.0;
  points.id = 0;
  line_strip.id = 1;
  goal_circle.id = 2;

  points.type = visualization_msgs::Marker::POINTS;
  line_strip.type = visualization_msgs::Marker::LINE_STRIP;
  goal_circle.type = visualization_msgs::Marker::CYLINDER;
  // POINTS markers use x and y scale for width/height respectively
  points.scale.x = 0.2;
  points.scale.y = 0.2;

  // LINE_STRIP markers use only the x component of scale, for the line width
  line_strip.scale.x = 0.1;

  goal_circle.scale.x = goalRadius;
  goal_circle.scale.y = goalRadius;
  goal_circle.scale.z = 0.1;

  // Points are green
  points.color.g = 1.0f;
  points.color.a = 1.0;

  // Line strip is blue
  line_strip.color.b = 1.0;
  line_strip.color.a = 1.0;

  // goal_circle is yellow
  goal_circle.color.r = 1.0;
  goal_circle.color.g = 1.0;
  goal_circle.color.b = 0.0;
  goal_circle.color.a = 0.5;
}

void L1Controller::odomCB(const nav_msgs::Odometry::ConstPtr &odomMsg)
{ //里程计回调函数
  odom = *odomMsg;
}


void L1Controller::pathCB(const nav_msgs::Path::ConstPtr &pathMsg)
{ //路径点回调函数
  //如果没路径了按上次路径走
  static int pathCBidx = 0;
  static nav_msgs::Path last_map_path;
  if (pathCBidx == 0)
  {
    last_map_path.poses.clear();
  }
  map_path = *pathMsg;
  mapPathNum = map_path.poses.size();
  if (map_path.poses.size() <= 0)
  {
    for (int i = 0; i < last_map_path.poses.size(); i++)
    {
      map_path.poses.push_back(last_map_path.poses[i]);
    }
  }
  else
  {
    last_map_path.poses.clear();
    for (int i = 0; i < map_path.poses.size(); i++)
    {
      last_map_path.poses.push_back(map_path.poses[i]);
    }
  }
  pathCBidx++;
}

/*void L1Controller::pathCB(const nav_msgs::Path::ConstPtr &pathMsg)
 { //路径点回调函数
   map_path = *pathMsg;
 }*/

void L1Controller::encoderCB(const nav_msgs::Odometry::ConstPtr &encoderMsg)
{ //编码器回调函数
  encoder = *encoderMsg;
}

void L1Controller::stopCB(const std_msgs::Float64::ConstPtr &stopMsg)
{
  stop_flag = (*stopMsg).data;
  ROS_INFO("stop_flag=%f", stop_flag);
  // stopIdx = stopIdx + 1;
}

void L1Controller::lineCB(const std_msgs::Float64::ConstPtr &lineMsg)
{
  line_wight = (*lineMsg).data;
  // stopIdx = stopIdx + 1;
}

void L1Controller::goalCB(const geometry_msgs::PoseStamped::ConstPtr &goalMsg)
{ //目标点回调函数
  try
  {
    geometry_msgs::PoseStamped odom_goal;
    tf_listener.transformPose("odom", ros::Time(0), *goalMsg, "map", odom_goal);

    odom_goal_pos = odom_goal.pose.position;
    goal_received = true;
    goal_reached = false;

    /*Draw Goal on RVIZ*/
    goal_circle.pose = odom_goal.pose;
    marker_pub.publish(goal_circle);
  }
  catch (tf::TransformException &ex)
  {
    ROS_ERROR("%s", ex.what());
    ros::Duration(1.0).sleep();
  }
}

double L1Controller::getYawFromPose(const geometry_msgs::Pose &carPose)
{ //计算航向角
  float x = carPose.orientation.x;
  float y = carPose.orientation.y;
  float z = carPose.orientation.z;
  float w = carPose.orientation.w;

  double tmp, yaw;
  tf::Quaternion q(x, y, z, w);
  tf::Matrix3x3 quaternion(q);
  quaternion.getRPY(tmp, tmp, yaw);

  return yaw;
}

bool L1Controller::isForwardWayPt(const geometry_msgs::Point &wayPt,
                                  const geometry_msgs::Pose &carPose)
{
  float car2wayPt_x = wayPt.x - carPose.position.x;
  float car2wayPt_y = wayPt.y - carPose.position.y;
  double car_theta = getYawFromPose(carPose);

  float car_car2wayPt_x = cos(car_theta) * car2wayPt_x + sin(car_theta) * car2wayPt_y;
  float car_car2wayPt_y = -sin(car_theta) * car2wayPt_x + cos(car_theta) * car2wayPt_y;

  if (car_car2wayPt_x > 0) /*is Forward WayPt*/
    return true;
  else
    return false;
}

bool L1Controller::isWayPtAwayFromLfwDist(const geometry_msgs::Point &wayPt, const geometry_msgs::Point &car_pos)
{ //判断是否是前瞻外的一个点
  double dx = wayPt.x - car_pos.x;
  double dy = wayPt.y - car_pos.y;
  double dist = sqrt(dx * dx + dy * dy);

  if (dist < Lfw)
    return false;
  else if (dist >= Lfw)
    return true;
  return 0;
}
// void callback(const art_racecar::racecarConfig &config, const uint32_t level)
// { //reconfigure配置动态参数
//   ROS_INFO("param changed");
//   L = config.L;
//   Vcmd = config.Vcmd;
//   Lfw = config.lfw;
//   controller_freq = config.controller_freq;
//   Angle_gain_p = config.Angle_gain_p;
//   Angle_gain_d = config.Angle_gain_d;
//   baseSpeed = config.baseSpeed;
//   k_rou = config.k_rou;
// }

geometry_msgs::Point L1Controller::get_odom_car2WayPtVec(const geometry_msgs::Pose &carPose)
{ //计算前瞻向量
  geometry_msgs::Point carPose_pos = carPose.position;
  double carPose_yaw = getYawFromPose(carPose);
  geometry_msgs::Point forwardPt;
  geometry_msgs::Point odom_car2WayPtVec;
  foundForwardPt = false;
  double car2goal_dist = getCar2GoalDist();
  bool start_flag = false;
  if (!goal_reached)
  {
    for (int i = 0; i < map_path.poses.size(); i++)
    {
      geometry_msgs::PoseStamped map_path_pose = map_path.poses[i];
      geometry_msgs::PoseStamped odom_path_pose;
      // geometry_msgs::PoseStamped odom_path_pose = map_path.poses[i];
      try
      {
        tf_listener.transformPose("odom", ros::Time(0), map_path_pose, "map", odom_path_pose);
        geometry_msgs::Point odom_path_wayPt = odom_path_pose.pose.position;
        bool _isForwardWayPt = isForwardWayPt(odom_path_wayPt, carPose);

        if (_isForwardWayPt && start_flag == false)
        {
          start_flag = true;
        }
        if (start_flag == false)
        {
          continue;
        }

        if (_isForwardWayPt || 1)
        {
          bool _isWayPtAwayFromLfwDist = isWayPtAwayFromLfwDist(odom_path_wayPt, carPose_pos);
          if (_isWayPtAwayFromLfwDist)
          {
            forwardPt = odom_path_wayPt;
            foundForwardPt = true;
            break;
          }
        }

        if (car2goal_dist < Lfw)
        {
          forwardPt = odom_goal_pos;
          foundForwardPt = true;
        }
      }
      catch (tf::TransformException &ex)
      {
        ROS_ERROR("%s", ex.what());
        ros::Duration(1.0).sleep();
      }
    }
  }
  else if (goal_reached)
  {
    forwardPt = odom_goal_pos;
    foundForwardPt = false;
    // ROS_INFO("goal REACHED!");
  }

  /*Visualized Target Point on RVIZ*/
  /*Clear former target point Marker*/
  points.points.clear();
  line_strip.points.clear();

  if (foundForwardPt && !goal_reached)
  {
    points.points.push_back(carPose_pos);
    points.points.push_back(forwardPt);
    line_strip.points.push_back(carPose_pos);
    line_strip.points.push_back(forwardPt);
  }

  marker_pub.publish(points);
  marker_pub.publish(line_strip);

  odom_car2WayPtVec.x = cos(carPose_yaw) * (forwardPt.x - carPose_pos.x) + sin(carPose_yaw) * (forwardPt.y - carPose_pos.y);
  odom_car2WayPtVec.y = -sin(carPose_yaw) * (forwardPt.x - carPose_pos.x) + cos(carPose_yaw) * (forwardPt.y - carPose_pos.y);
  return odom_car2WayPtVec;
}

double L1Controller::getEta(const geometry_msgs::Pose &carPose)
{ //根据前瞻向量求车到前瞻点和车中心线的夹角
  geometry_msgs::Point odom_car2WayPtVec = get_odom_car2WayPtVec(carPose);
  double eta = atan2(odom_car2WayPtVec.y, odom_car2WayPtVec.x);
  return eta;
}

double L1Controller::getCar2GoalDist()
{ //计算车到目标点的距离
  geometry_msgs::Point car_pose = odom.pose.pose.position;
  double car2goal_x = odom_goal_pos.x - car_pose.x;
  double car2goal_y = odom_goal_pos.y - car_pose.y;
  double dist2goal = sqrt(car2goal_x * car2goal_x + car2goal_y * car2goal_y);
  return dist2goal;
}

double L1Controller::getL1Distance(const double &_Vcmd)
{ //根据速度变前瞻距离
  double L1 = 0;
  double car2goal_dist = getCar2GoalDist();
  double v = _Vcmd;
  /*if (car2goal_dist < 1)
  {
   L1 = 0.5; 
  }
  else
  {*/
  L1 = 1.45;
  //}
  // L1 = 0.65 + 0.6 * _Vcmd;

  return L1;
}

double L1Controller::getSteeringAngle(double eta)
{ //纯追踪算舵机打角
  double steeringAnge = atan2((L * sin(eta)), ((Lfw / 2) + lfw * cos(eta))) * (180.0 / PI);
  // ROS_INFO("Steering Angle = %.2f", steeringAnge);
  return steeringAnge;
}

void L1Controller::goalReachingCB(const ros::TimerEvent &)
{ //小车到达目标点后

  if (goal_received)
  {
    double car2goal_dist = getCar2GoalDist();
    if (car2goal_dist < goalRadius)
    {
      goal_reached = true;
      goal_received = false;
      cmd_vel.linear.x = 0.0;
      cmd_vel.angular.z = 0.0;
      pub_.publish(cmd_vel);
      ROS_INFO("Goal Reached !!!!!!!");
    }
  }
}

double L1Controller::isline(double line_wight)
{
  if (line_wight == 0.0)
  {
    return initbaseSpeed;
  }
  double line_acc = 0.0;
  //tow versions
  line_acc = line_wight * 0.5;
  baseSpeed = baseSpeed + line_acc;
  ROS_WARN("WE ARE CHAMPION!!!!!!!!!!!!");
  return baseSpeed;
}
void L1Controller::controlLoopCB(const ros::TimerEvent &)
{

  geometry_msgs::Pose carPose = odom.pose.pose;
  geometry_msgs::Twist carVel = odom.twist.twist;
  cmd_vel.linear.x = 0;
  cmd_vel.angular.z = baseAngle;
  double encoder_speed = encoder.twist.twist.linear.x;
  static double speedlast;
  static double anglelast;
  //Lfw = getL1Distance(encoder_speed);
  if (goal_received)
  {
    double eta = getEta(carPose);
    if (foundForwardPt)
    {
      if (!goal_reached)
      {
        if (stop_flag == 1.0 && stopIdx <= 0)
        {
          //only ex once
          baseSpeed = slow_final * baseSpeed + 1500;
          stopIdx++;
          ROS_WARN("I GET THE FINAL GOAL AND I WILL SLOW DOWN");
        }
        if (stop_flag == 2.0 && stopIdx <= 0)
        {
          //only ex once
          baseSpeed = fast_final * baseSpeed + 1500;
          stopIdx++;
          ROS_WARN("I GET THE FINAL GOAL AND I WILL SPEED UP");
        }
        if (stop_flag == 3.0 && stopIdx > 0)
        {
          baseSpeed = initbaseSpeed + 1500;
          ROS_WARN("I recovery the speed in case overstep the area");
        }
        cmd_vel.linear.x = baseSpeed;
        cmd_vel.angular.z = 90 - getSteeringAngle(eta) * Angle_gain_p - Angle_gain_d * (getSteeringAngle(eta) - last_steeringangle); //纯追踪pd
        last_steeringangle = getSteeringAngle(eta);

        //角度限幅

        if (cmd_vel.linear.x < vp_min+1500)
          cmd_vel.linear.x = vp_min+1500;
        if (mapPathNum <= 0)
        {
          //if now the path is empty then v=kv
          ROS_WARN("---------------NO PATH TO GO");
          cmd_vel.linear.x = 115;
          //cmd_vel.angular.z = anglelast + 0.1;
        }
        if (cmd_vel.linear.x > vp_max_base+1500)
          cmd_vel.linear.x = vp_max_base+1500;

        if (cmd_vel.angular.z > 135)
          cmd_vel.angular.z = 135;
        else if (cmd_vel.angular.z < 45)
          cmd_vel.angular.z = 45;

        ROS_INFO("Lfw = %.2f", Lfw);
        ROS_INFO("eta = %.2f", eta * 180 / PI);
        ROS_INFO("encoder_v = %.2f", encoder_speed);
        ROS_INFO("out_speed = %.2f", cmd_vel.linear.x);
        ROS_INFO("out_angle = %.2f", cmd_vel.angular.z);
        ROS_INFO("------------------------");
      }
    }
  }
  else
  {
    cmd_vel.linear.x = 1500;
    cmd_vel.angular.z = 90;
    //ROS_INFO("Goal_Reached!!!");
  }
  speedlast = cmd_vel.linear.x;
  anglelast = cmd_vel.angular.z;
  pub_.publish(cmd_vel);
}

/*****************/
/* MAIN FUNCTION */
/*****************/
int main(int argc, char **argv)
{
  // Initiate ROS
  ros::init(argc, argv, "art_car_controller");
  L1Controller controller;

  ros::spin();
  return 0;
}
```
这个程序放上来纯粹是为了以后万万一有空想起来了看一眼

下面说我自己的。首先是路线规划到底是什么，在rviz打开`poseArray`然后选择`/move_base/TebLocalPlannerROS/teb_poses`这个topic，可以看到很多向量，这就是车子要走过的每一个点，我们可以根据这个点来规划车子行进
![规划的路径点](微信截图_20230608201239.png)
![teb发布的其他话题](微信截图_20230608201807.png)
或者直接用命令查看话题内容：
```sh
rostopic echo /move_base/TebLocalPlannerROS/local_plan
```
![一大串坐标点和四元数方向](微信截图_20230608203032.png)

好了差不多了开始写

这个程序问题还是很大的，比如显然反正切值和舵机角度之间关系不是线性的，甚至没有正负判断，仅用于举例体现如何实现，以后用到务必修改

run.py：
```python
import rospy
from geometry_msgs.msg import PoseArray, Twist
from scipy.spatial.transform import Rotation as R
import tf
import math


def get_dir(PoseArray):
    global tf_listener, cmd_pub
    # 获取teb规划的下一个点的位置
    if len(PoseArray.poses) > 5:
        pose_next = PoseArray.poses[5]
    else:
        pose_next = PoseArray.poses[-1]
    print("next_pose:", pose_next.position)
    print("-------------------------------------")
    # rospy_Time(0)指最近时刻,从 /map 到 /base_link 的变换，也就是车目前的坐标
    (trans, rot) = tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
    # 四元数转欧拉角转弧度
    r = R.from_quat(rot)
    euler_z = math.radians(r.as_euler('xyz', degrees=True)[2])
    print("now_pose:", trans[0], trans[1], euler_z)
    print("-------------------------------------")
    # 比较arctan值计算舵机方向，差为负则左转
    arg_next = math.atan2(pose_next.position.y, pose_next.position.x)
    arg_now = math.atan2(trans[1], trans[0])
    arg_d = arg_now - arg_next
    print("arg:", arg_d)
    print("-------------------------------------")
    # 向底盘控制节点发送信息
    twist = Twist()
    twist.linear.x = 1500 + 200
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 90 - 10000*arg_d
    cmd_pub.publish(twist)
    print(90 - 10000*arg_d)


if __name__ == '__main__':
    # 订阅teb的坐标话题，回调函数get_dir
    rospy.init_node('teb_pos_subscriber', anonymous=True)
    tf_listener = tf.TransformListener()
    cmd_pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=5)
    rospy.Subscriber("/move_base/TebLocalPlannerROS/teb_poses", PoseArray, get_dir)
    rospy.spin()

```

没有继续完善上面程序的原因就是......志伟哥已经写好了路径点纯追踪的程序，如果想要实现导航功能，把路径点读取改成获取导航坐标点就可以了

pp.py:
```python
from geometry_msgs.msg import PoseArray
from sklearn.metrics import pairwise_distances
import rospy
import tf2_ros
import numpy as np
import math
import time
from geometry_msgs.msg import Twist
import json
from scipy.interpolate import splprep, splev

class PurePursuit:
    def __init__(self):
        self.path_list = []
        self.final_point = None
        self.load_path()

        self.speed_mid = 1500
        self.speed_max = 350
        self.speed_max_final = 280
        self.pp_k = 0.9


        self.tf_buffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(self.tf_buffer)
        self.cmd_pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=5)
        self.start_time = rospy.Time.now()

    def load_path(self):
        x = [0]
        y = [0]
        with open('/home/ros-autocar/Ros-manualcar/src/autopilot/scripts/waypoint.json', 'r') as f:
            data = json.load(f)
            f.close()
        waypoint = data["waypoint"]
        for point in waypoint:
            x.append(point[0])
            y.append(point[1])
        tck, u = splprep([x, y], s=0)
        u_new = np.linspace(u.min(), u.max(), 200)
        x_new, y_new = splev(u_new, tck)
        for i in range(len(x_new)):
            self.path_list.append([x_new[i], y_new[i]])
        self.final_point = self.path_list[-1]

    def run(self):
        while not rospy.is_shutdown():
            time.sleep(0.01)


            try:
                trans = self.tf_buffer.lookup_transform("map", 'base_link', rospy.Time())
            except:
                print("missing tf2 trans")
                continue
            x = trans.transform.translation.x
            y = trans.transform.translation.y

            if len(self.path_list) < 10:
                dis_final = math.sqrt((self.final_point[0] - x) ** 2 + (self.final_point[1] - y) ** 2)
                self.speed_max = self.speed_max_final
                print(f"final distance: {dis_final}")
                if dis_final < 0.7:
                    twist = Twist()
                    twist.linear.x = 1500
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 90
                    self.cmd_pub.publish(twist)
                    print("arrive")
                    break
            
            if len(self.path_list) == 0:
                continue

            degree = self.quaternion_to_euler_angle(trans.transform.rotation.w,
                                                    trans.transform.rotation.x,
                                                    trans.transform.rotation.y,
                                                    trans.transform.rotation.z,)
            degree = degree / 180 * math.pi

            for i in range(len(self.path_list)):
                distance = math.sqrt((self.path_list[i][0] - x) ** 2 + (self.path_list[i][1] - y) ** 2)
                if distance > self.pp_k:
                    self.path_list = self.path_list[i:]
                    break

            forward_point = [self.path_list[0]]

            a = forward_point[0][0]-x
            b = forward_point[0][1]-y

            theta = math.acos(a / math.sqrt(a * a + b * b))
            if b < 0:
                theta = - theta
            theta -= degree

            wheel_angle = 0.9*math.atan(2 * 0.3 * math.sin(theta) / self.pp_k * 2.15) / math.pi * 180
            speed = self.speed_mid + self.speed_max

            print(f"angle: {wheel_angle},speed:{speed},points:{len(self.path_list)}")

            twist = Twist()
            twist.linear.x = speed
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 90+wheel_angle

            self.cmd_pub.publish(twist)


    def quaternion_to_euler_angle(self,w, x, y, z):
        ysqr = y * y
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        Z = np.degrees(np.arctan2(t3, t4))

        return Z


rospy.init_node('pp')
pp = PurePursuit()
pp.run()

```

## 区域搜索：RRT
