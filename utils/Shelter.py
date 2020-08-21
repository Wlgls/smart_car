#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:Shelter.py
@Time			:2020/08/16 22:47:33
@Author			:wlgls
@Version		:1.0
@Abstract       :           
'''

'''
使用逻辑模式实现蔽障程序的设计，即手动的通过获得超声波和红外线的方法来判断
接下来小车的运行状态。
'''

import RPi.GPIO as GPIO
from Car import Car
from Ultrasound import Ultrasound
from Infrared import Infrared
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class CarMove(Car, Ultrasound, Infrared):
    def __init__(self):
        Car.__init__(self)
        Ultrasound.__init__(self)  
        Infrared.__init__(self)
    
    def Astop(self):
        Car.stop(self)
        GPIO.cleanup()

def main():
    try:
        Cr = CarMove()
        start_time = None
        while True:
            time.sleep(2)
            dist = Cr.compute_dist()
            print(dist)
            left, right = Cr.obstacle_measure().values()
            print(left, right)
            left = False
            if start_time is None or time.time()-start_time > 0.5:
                start_time = None
                if left and not right:
                    print("right")
                    Cr.turn_right()
                elif not left and right:
                    print("left")
                    Cr.turn_left()
                elif left and right:
                    print("back")
                    Cr.back()
                else:
                    if dist < 20:
                        Cr.turn_right()
                        start_time = time.time()
                    else:
                        print("forward")
                        Cr.forward()

    except KeyboardInterrupt:
        Cr.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()



