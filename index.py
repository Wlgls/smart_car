from bottle import get,post,run,request,template

from utils.Car import Car

car = Car()

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

@get("/")
def index():
    return template("templates/index")

@post("/cmd")
def cmd():
    status = request.body.read().decode()
    print("按下了按钮: "+request.body.read().decode())
    main(status)
    #return "OK"
run(host="0.0.0.0",port="8080")