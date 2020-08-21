#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:testcar.py
@Time			:2020/08/21 15:10:51
@Author			:wlgls
@Version		:1.0
@Abstract       :测试小车运行，运行时间１分钟，不断前进，后退，右转，左转
'''
import sys
sys.path.append('/home/pi/pi')
from utils.Car import Car
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


if __name__ == "__main__":
    try:
        Cr = Car()
        start = time.time()
        print(start)
        # while True:
    except KeyboardInterrupt:
        Cr.stop()
        GPIO.cleanup()


