#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:controlSpeel.py
@Time			:2020/08/26 10:30:24
@Author			:wlgls
@Version		:1.0
@Abstract       :用于测试小车控速
'''

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



ENA=13
IN1=19
IN2=26
ENB=21
IN3=16
IN4=20
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

pwm1 = GPIO.PWM(ENA, 500)
pwm2 = GPIO.PWM(ENB, 500)

pwm1.start(50)
pwm2.start(50)
GPIO.output([IN1, IN3], GPIO.LOW)
GPIO.output([IN2, IN4], GPIO.HIGH)
time.sleep(2)
print("go")

""" for i in range(11):
    pwm1.ChangeDutyCycle(10 * i)
    pwm2.ChangeDutyCycle(10 * i)
    time.sleep(2)
    print(i, "'s speed up") """

print("over")

GPIO.output([IN1,IN2, IN3, IN4], GPIO.LOW)
GPIO.cleanup()
pwm1.stop()
pwm2.stop()


