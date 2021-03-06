#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:infrared.py
@Time			:2020/07/25 22:27:47
@Author			:wlgls
@Version		:1.0
'''

'''
说明:
红外线检测，将两个红外线放在小车两侧用于检测两侧的障碍物
三引脚，其中vcc接L298N的5V输出，gnd接L298N的地
右侧红外output:GPIO-10
左侧红外output:GPIO-9
有障碍时输入为0， 返回为True
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Infrared(object):
    def __init__(self):
        self.left_infrared = 10
        self.right_infrared = 9
        GPIO.setup(self.right_infrared, GPIO.IN)
        GPIO.setup(self.left_infrared, GPIO.IN)
    
    def obstacle_measure(self):
        """检查是否有障碍物
        """
        left_measure = False if GPIO.input(self.left_infrared) else True
        right_measure = False if GPIO.input(self.right_infrared) else True
        return {"left":left_measure, "right":right_measure}

if __name__ == "__main__":
    infrared = Infrared()
    while True:
        print(infrared.obstacle_measure())