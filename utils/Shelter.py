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

这个继承有点问题，在index中继承之后，还要继承，就会出现错误，所以，将其放在index

'''

import RPi.GPIO as GPIO
from Car import Car
from Ultrasound import Ultrasound
from Infrared import Infrared
import time
import threading
import csv
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Shelter(Car, Ultrasound, Infrared):
    def __init__(self):
        Car.__init__(self, 100)
        Ultrasound.__init__(self)  
        Infrared.__init__(self)
        self.Thread = None
        self.flag = True
        self.d = None
        self.l = None
        self.r = None
        self.t = None

    def Str(self):
        if self.Thread is None:
            self.flag = True
            self.Thread = threading.Thread(target=self._thread)
            self.Thread.setDaemon(True)
            self.Thread.start()

    def _thread(self):
        start_time = None
        while self.flag:
            dist = self.compute_dist()
            print(dist)
            left, right = self.obstacle_measure().values()
            self.d = dist
            self.l =left 
            self.r = right
            print(left, right)
            if start_time is None or time.time()-start_time > 0.5:
                start_time = None
                if left and not right:
                    print("right")
                    self.t = 'tr'
                    self.turn_right()
                elif not left and right:
                    print("left")
                    self.t = 'tl'
                    self.turn_left()
                elif left and right:
                    print("back")
                    self.t = 'b'
                    self.back()
                else:
                    if dist < 20:
                        print("right")
                        self.t = 'tr'
                        self.turn_right()
                        start_time = time.time()
                    else:
                        self.t = 'f'
                        print("forward")
                        self.forward()
        print("thread stop")
        
    def stopshelter(self, flag=False):
        self.flag = flag
        self.Thread = None
        self.stop()
        time.sleep(2)

    def capture(self):
        path = '/home/pi/data.csv'
        with open(path, 'w') as f:
            csv_write =csv.writer(f)
            csv_head = ['left', 'right', 'dist', 'cont']
            csv_write.writerow(csv_head)
        
        with open(path, 'a+') as f:
            csv_write = csv.writer(f)
            while True:
                data = [self.l, self.r, self.d, self.t]
                csv_write.writerow(data)
                time.sleep(1)

            
            
def main():
    try:
        Cr = Shelter()
        Cr.Str()
        Cr.capture()
    except KeyboardInterrupt:
        Cr.stopshelter()
        GPIO.cleanup()

if __name__ == "__main__":
    main()



