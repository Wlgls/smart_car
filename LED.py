import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED_R = 21
LED_G = 26


GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.output(LED_G, GPIO.HIGH)
#GPIO.output(LED_G, GPIO.LOW)
time.sleep(8)
GPIO.output(LED_R, GPIO.LOW)
GPIO.output(LED_G, GPIO.HIGH)
time.sleep(8)
GPIO.cleanup()
