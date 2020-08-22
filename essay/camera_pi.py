from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()
for i in range(5):
    time.sleep(5)
    camera.capture("/home/pi/image%s.jpg" % i)
camera.stop_preview()
