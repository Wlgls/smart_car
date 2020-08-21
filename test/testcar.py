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

def testall():
    try:
        Cr = Car()
        start = time.time()
        while time.time() - start < 60:
            print("forward")
            Cr.forward()
            time.sleep(1)
            print("back")
            Cr.back()
            time.sleep(1)
            print("right")
            Cr.turn_right()
            time.sleep(1)
            print("turn_left")
            Cr.turn_left()
            time.sleep(1)
    except KeyboardInterrupt:
        Cr.stop()
        GPIO.cleanup()

def testleft():
    Cr = Car()
    Cr.turn_left()
    time.sleep(2)
    Cr.stop()
    GPIO.cleanup()

def testspeed():
    try:
        Cr = Car(10)
        Cr.forward()
        time.sleep(2)
        Cr.stop()
        time.sleep(1)

    except KeyboardInterrupt:
        Cr.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    # testleft()
    # testall()
    testspeed()