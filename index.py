from flask import Flask, request, render_template
from car import Car

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cmd", methods=["GET", "POST"])
def cmd():
    addss = request.get_data()
    print(addss.decode())
    main(addss.decode())
    return "Ok"
app.run(host="0.0.0.0")