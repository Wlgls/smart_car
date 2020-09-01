#-*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.getcwd()+"/utils")
print(sys.path)
from flask import Flask, request, render_template, Response
from utils.Car import Car
from utils.camera_pi import Camera
from utils import object_detect

app = Flask(__name__)

car = Car()
od = object_detect.object_Detect()

def main(status):
    print(status)
    if status == "front":
        car.forward()
    elif status == "leftFront":
        car.turn_left()
    elif status == "rightFront":
        car.turn_right()
    elif status == "rear":
        car.back()
    elif status == "leftRear":
        car.turn_left_back()
    elif status == "rightRear":
        car.turn_right_back()
    elif status == "stop":
        car.stop()

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
    return Response(gen(od), 
            mimetype="multipart/x-mixed-replace;boundary=frame")
            

@app.route("/cmd", methods=["GET", "POST"])
def cmd():
    addss = request.get_data()
    print(addss.decode())
    main(addss.decode())
    return "Ok"

app.run(host="0.0.0.0")
