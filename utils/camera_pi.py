#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:camera_pi.py
@Time			:2020/09/02 21:08:08
@Author			:wlgls
@Version		:1.0
@Abstract       :照相机以及网球检测，但是网球检测似乎无法成功
'''
import time
import io
import threading
import picamera
import os
from picamera.array import PiRGBArray
import cv2
import numpy as np
import copy
import socket
from Car import Car
import RPi.GPIO as GPIO

class Camera(object):
    
    def __init__(self, tennis_detect=False):
        self.count = 0
        self.tennis_detect = tennis_detect
        self.thread = None  # background thread that reads frames from camera
        self.frame = None  # current frame is stored here by background thread
        self.last_access = 0  # time of last client access to the camera
        self.pos = None
        self.lower = np.array([40, 90, 160])
        self.higher = np.array([55, 110, 200])


        self.status = None
        self.tennisrun = False

        # 控制小车
        self.center_x = 1280/2
        self.center_y = 720/2
        self.center_r = 80

        # 阈值
        self.limit_x = 150
        self.limit_y = 150
        self.limit_r = 10

        HOST = '192.168.1.102'  # ip of PC
        PORT = 8000  # 随便设置一个，对应起来就行
        self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.connect((HOST,PORT))


    def settennisrun(self, flag=False):
        self.tennisrun = flag
        time.sleep(1)
        
    def runcamera(self):
        if self.thread is None:
            # start background frame thread
            print("new thread")
            self.thread = threading.Thread(target=self._thread)
            self.thread.setDaemon(True)
            self.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
        
    
    def transform(self, frame):
        success, imagecode = cv2.imencode(".jpeg", frame)
        return imagecode, self.pos

    def tennis_detecter(self, img):
        # print("1")
        img = cv2.GaussianBlur(img, (5, 5), 5)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        edge = cv2.Canny(gray_img, 5, 20)
        circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 60, param1=100, param2=30,minRadius=60, maxRadius=120)
        # print(circles)
        # fig, ax = plt.subplots(3, 4)
        if circles is not None:
            x = circles[0][:, 0].astype(int)
            y = circles[0][:, 1].astype(int)
            r = circles[0][:, 2].astype(int)
            s_r = (r/1.5).astype(int)
            num = len(circles[0])
            rate = np.zeros(num)
            # print(num)
            for i in range(num):
                detect_area = (hsv_img[y[i]-s_r[i]:y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])
                # ax[i//5][i%5].imshow(detect_area, cmap=plt.cm.hsv)
                height, width, channel = detect_area.shape
                if height != 0 and width != 0:
                    tennis_color_mask = cv2.inRange(detect_area, self.lower, self.higher)
                    num_point = np.sum(tennis_color_mask/255)
                    rate[i] = num_point / (height * width)
                    #img_out = cv2.circle(img, (x[i], y[i]), r[i], (255, 0, 0), thickness=2)
                    #ax[i//4][i%4].imshow(img_out)
            i = np.argmax(rate)
            x_pos = x[i]
            y_pos = y[i]
            radius = r[i]
            img_out = cv2.circle(img, (x_pos, y_pos), radius, (255, 0, 0), thickness=10)
            return img_out, (x_pos, y_pos, radius)
        return img, None
        
    def get_frame(self):
        # 返回array数组
        self.last_access = time.time()
        self.runcamera()
        return self.transform(self.frame)

    def testframe(self):
        self.last_access = time.time()
        self.runcamera()
        return None

    def _thread(self):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (1280, 720)
            camera.rotation = 180
            camera.hflip = True
            camera.vflip = True
            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = PiRGBArray(camera)
            for foo in camera.capture_continuous(stream, 'bgr',
                                                 use_video_port=True):
                if self.tennisrun:
                    # self.frame = stream.array
                    # print("start detect")
                    frame, postision = self.tennis_detecter(foo.array)
                    # print("end detect")
                    # print(frame.shape)
                    # self.VideoTransmission(np.copy(foo.array))
                    self.frame = frame
                    self.pos = postision
                    if postision:
                        time.sleep(2)
                        self.controlcar(*postision)
                else:
                    self.frame = foo.array
                # self.saveimg(frame)

                stream.truncate(0)
                #print(stream)
                if time.time() - self.last_access > 10:
                    break   
        self.thread = None 

    def saveimg(self, frame):
        path = '/home/pi/img/'
        cv2.imwrite(path+'img{}.jpg'.format(self.count), frame)
        self.count+=1

    def controlcar(self, posx, posy, posr):
        print(posx, posy, posr)

        if posr - self.center_r > self.limit_r:
            print('back')
            self.back()
            time.sleep(0.2)
            self.stop()
        elif self.center_r - posr > self.limit_r:
            print('forward')
            self.forward()
            time.sleep(0.2)
            self.stop()
        if posx - self.center_x > self.limit_x:
            print('turnr')
            self.turn_right(25)
        elif self.center_x - posx > self.limit_x:
            print('turnl')
            self.turn_left(25)

        return None

    def VideoTransmission(self, frame):  # transmit video from Pi to PC
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])  #编码
        try:
            self.server.sendall(struct.pack('i',imgencode.shape[0]))  # 发送数据长度作为校验
            self.server.sendall(imgencode)
            print("have sent one frame")
        except:
            print("fail to send the frame")


if __name__ == "__main__":
    try:
        c = Camera()
        c.settennisrun(True)
        while True:
            data = c.get_frame()
        
    except KeyboardInterrupt:
        GPIO.cleanup()

        
    # print(type(data))
    
