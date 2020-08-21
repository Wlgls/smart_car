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

if __name__ == "__main__":
    GPIO.cleanup()
    try:
        Cr = CarMove()
        Cr.forward()
        while True:
            print(Cr.obstacle_measure())
            time.sleep(2)
    except KeyboardInterrupt:
        Cr.Astop()
