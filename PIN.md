

#### Car

* ENA:GPIO-13
* IN1:GPIO-19
* IN2:GPIO-26
* ENB:GPIO-21
* IN3:GPIO-16
* IN4:GPIO-20

out1,3 后下

实现了car类，主要有forward，back，stop等类，无返回值

#### infrared

* 左侧 output: GPIO-10
* 右侧 output:GPIO-9

实现了Infrared类，主要函数是obstacle_measure，返回左侧和右侧是否有障碍物，有则为True。

#### Ultrasound

* vcc:5v
* gnd:gnd
* trig:GPIO-2
* echo:GPIO-3

实现了Ultrasound类，主要函数是compute_dist。返回前方障碍物的距离。

#### 舵机

* vcc:5v
* signal:GPIO-12

实现了SteeringEng类，主要函数是rotate，用于旋转。

#### 风扇

* vcc:5V

* E极:GND
* B级:GPIO-14

