#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:testinfrared.py
@Time			:2020/08/21 15:48:16
@Author			:wlgls
@Version		:1.0
@Abstract       :测试红外线，运行时间30s
'''

import sys
sys.path.append("/home/pi/pi")
from utils.Infrared import Infrared
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def testinf():
    try:
        inf = Infrared()
        start = time.time() 
        while time.time() - start < 30:
            print(inf.obstacle_measure())
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    
if __name__ == "__main__":
    testinf()


