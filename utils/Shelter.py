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
import Car, Ultrasound, Infrared
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def main():
    Cr = Car.Car()
    Usd = Ultrasound.Ultrasound()
    Ird = Infrared.Infrared()

    Cr.forward()

    safedist = 40
    try:
        while True:
            time.sleep(1)
            Cr.stop()
            dist = Usd.compute_dist()
            left, right = Ird.obstacle_measure().values()
            print(dist)
            print(left, right)
            if dist < safedist:
                if not left and not right:
                    # Cr.back()
                    Cr.turn_right()
                if left and not right:
                    print("turn_right")
                    Cr.turn_right()
                if not left and right:
                    print("turn_left")
                    Cr.turn_left()
                if left and right:
                    print("back")
                    Cr.back()
                    if left and not right:
                        time.sleep(1)
                        print("turn_right")
                        Cr.turn_right()
                    if not left and right:
                        time.sleep(1)
                        print("turn_left")
                        Cr.turn_left()
            else:
                print("forward")
                Cr.forward()
    except KeyboardInterrupt:
        Cr.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()



