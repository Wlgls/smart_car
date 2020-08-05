#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:Ultrasound.py
@Time			:2020/07/23 21:17:11
@Author			:wlgls
@Version		:1.0
'''

'''
超声波模块
用于避障，超声波一共四个引脚，其中vcc接5V电压，gnd接地
trig引脚接收来自树莓派的控制信号
echo引脚用来发送测距结果给树莓派
trig: GPIO-2
echo: GPIO-3
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Ultrasound(object):
    def __init__(self):
        self.trig = 2
        self.echo = 3
        GPIO.setup(self.trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo, GPIO.IN)

    def compute_dist(self):
        """计算距离
        """
        # 先送一个10us的正脉冲
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(1e-5)
        GPIO.output(self.trig, GPIO.LOW)

        #轮询法判断送进来的正脉冲时间，即为来回时间
        while not GPIO.input(self.echo):
            pass
        t1 = time.time()
        while GPIO.input(self.echo):
            pass
        t2 = time.time()
        dist = (t2-t1) * 340*100/2

        # GPIO.cleanup()
        return round(dist, 2)

if __name__ == "__main__":
    U = Ultrasound()
    print("{:.2f}cm".format(U.compute_dist()))
    

        
        