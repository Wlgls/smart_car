#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:angleServoCtrl.py
@Time			:2020/07/30 20:37:34
@Author			:wlgls
@Version		:1.0
@Abstract       :用于控制舵机
                signal:GPIO-12
                本舵机是连续旋转的，所以使用时间来控制旋转角度
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class SteeringEng(object):
    def __init__(self):
        self.signal = 12
        GPIO.setup(self.signal, GPIO.OUT)
        self.inlt = GPIO.PWM(self.signal, 50)
        self.inlt.start(0)

    def rotate(self, angel):
        self.inlt.ChangeDutyCycle(2)
        time.sleep(0.3*angel/180)
        self.inlt.ChangeDutyCycle(0)

    def cleanup(self):
        self.inlt.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    stre = SteeringEng()
    stre.rotate(90)
    stre.cleanup()

