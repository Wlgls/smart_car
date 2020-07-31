#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:car.py
@Time			:2020/07/23 16:31:55
@Author			:wlgls
@Version		:1.0
'''
"""
说明:
一个L298N控制4个直流电机，即同侧并联
其中ENA和IN1和IN2控制A一侧(右侧)，ENAB和IN3和IN4控制B一侧(左侧)
暂未实现调速
基于不同的连线，函数可能发生变换，如前进变为后退等
具体连线为（BCM）:
ENA:GPIO-13
IN1:GPIO-19
IN2:GPIO-26
ENB:GPIO-21
IN3:GPIO-20
IN4:GPIO-16
"""


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Car(object):

    def __init__(self):
        self.ENA=13
        self.IN1=19
        self.IN2=26
        self.ENB=21
        self.IN3=20
        self.IN4=16
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)

    def _reset(self):
        """初始化小车，用于复位和停止运行
        """
        GPIO.output(self.ENA, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.ENB, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
    
    def _left_forward(self):
        """左侧齿轮向前
        """
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)

    def _right_forward(self):
        """由测齿轮向前
        """
        GPIO.output(self.ENB, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
    
    def _left_back(self):
        """左侧齿轮向后
        """
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
    
    def _right_back(self):
        """右侧齿轮向后
        """
        GPIO.output(self.ENB, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self):
        """前进
        """
        self._reset()
        self._left_forward()
        self._right_forward()

    def back(self):
        """后退
        """
        self._reset()
        self._right_back()
        self._left_back()
    
    def turn_left(self):
        """左转
        """
        self._reset()
        self._right_forward()
        time.sleep(1)
        self._reset()
    
    def turn_right(self):
        """右转
        """
        self._reset()
        self._left_forward()
        time.sleep(1)
        self._reset()

    def stop(self):
        self._reset()

    def turn_left_back(self):
        """左后
        """
        self._reset()
        self._right_back()
        time.sleep(1)
        self._reset()
    def turn_right_back(self):
        """右后
        """
        self._reset()
        self._left_back()
        time.sleep(1)
        self._reset()

if __name__ =="__main__":
    car = Car()
    car.back()
    time.sleep(2)
    car.stop()
    
    
        


        
        

