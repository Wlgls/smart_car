#-*- coding:utf-8 -*-
import sys
import os
import threading
sys.path.append(os.getcwd()+"/utils")
from flask import Flask, request, render_template, Response
from utils.Car import Car
from utils.camera_pi import Camera
from utils.Ultrasound import Ultrasound
from utils.Infrared import Infrared
# from utils import object_detect
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

class CMove(Car, Ultrasound, Infrared, Camera):
    def __init__(self):
        # Car.__init__(self, 80)
        Ultrasound.__init__(self)
        Infrared.__init__(self)
        Camera.__init__(self, tennis_detect=False)
        self.ShrThread = None
        self.flag = False

    def startShelter(self):
        if self.ShrThread is None:
            self.flag = True
            self.ShrThread = threading.Thread(target=self._Shrthread)
            self.ShrThread.setDaemon(True)
            self.ShrThread.start()

    def _Shrthread(self):
        start_time = None
        while self.flag:
            dist = self.compute_dist()
            print(dist)
            left, right = self.obstacle_measure().values()
            print(left, right)
            if start_time is None or time.time()-start_time > 0.5:
                start_time = None
                if left and not right:
                    print("right")
                    self.turn_right()
                elif not left and right:
                    print("left")
                    self.turn_left()
                elif left and right:
                    print("back")
                    self.back()
                else:
                    if dist < 20:
                        print("right")
                        self.turn_right()
                        start_time = time.time()
                    else:
                        print("forward")
                        self.forward()
        print("thread stop")
    
    def setflag(self, flag=False):
        self.flag = flag
        self.ShrThread = None
        self.stop()
        time.sleep(2)

    def AllStop(self):
        self.stopcar(self)
        self.setflag(False)
        GPIO.cleanup()

CMove = CMove()

def main(status):
    print(status)
    if status != 'shelter' and status != 'stopshelter':
        if CMove.flag:
            CMove.setflag()
        if status == "front":
            CMove.forward()
        elif status == "leftFront":
            CMove.turn_left()
        elif status == "rightFront":
            CMove.turn_right()
        elif status == "rear":
            CMove.back()
        elif status == "leftRear":
            CMove.turn_left_back()
        elif status == "rightRear":
            CMove.turn_right_back()
        elif status == "stop":
            CMove.stop()
    else:
        print("test")
        if status == 'shelter':
            CMove.startShelter()
        else:
            CMove.setflag(False)

@app.route("/")
def index():
    return render_template("index.html")

def gen(camera):
    while True:
        frame, _ = camera.get_frame()
        frame = frame.tobytes()
        yield (b"--frame\r\n"
                b"Content-Type:image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(CMove), 
            mimetype="multipart/x-mixed-replace;boundary=frame")
            

@app.route("/cmd", methods=["GET", "POST"])
def cmd():
    addss = request.get_data()
    #print(addss.decode())
    main(addss.decode())
    return "Ok"
try:
    app.run(host="0.0.0.0")
except KeyboardInterrupt:
    CMove.AllStop()