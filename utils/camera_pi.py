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


class Camera(object):
    
    def __init__(self, tennis_detect=False):
        self.tennis_detect = tennis_detect
        self.thread = None  # background thread that reads frames from camera
        self.frame = None  # current frame is stored here by background thread
        self.last_access = 0  # time of last client access to the camera
        self.position = None
        self.lower = np.array([35, 130, 80])
        self.higher = np.array([50, 170, 140])

    def initialize(self):
        if self.thread is None:
            # start background frame thread
            print("new thread")
            self.thread = threading.Thread(target=self._thread)
            self.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
                
    def transform(self, frame):
        if self.tennis_detect:
            frame, self.position = self.tennis_detecter(frame)
        success, imagecode = cv2.imencode(".jpeg", frame)
        return imagecode, self.position

    def tennis_detecter(self, frame):
        # print("1")
        img = copy.copy(frame)
        img = cv2.GaussianBlur(img, (5, 5), 5)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        edge = cv2.Canny(gray_img, 10, 30)
        circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 60, param1=100, param2=20, minRadius=100, maxRadius=400)
        # print(circles)
        if circles is not None:
            x = circles[0][:, 0].astype(int)
            y = circles[0][:, 1].astype(int)
            r = circles[0][:, 2].astype(int)
            s_r = (r/1.5).astype(int)
            num = len(circles[0])
            rate = np.zeros(num)
            #print(num)
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
            if rate[i] > 0.4:
                x_pos = x[i]
                y_pos = y[i]
                radius = r[i]
                img_out = cv2.circle(img, (x_pos, y_pos), radius, (255, 0, 0), thickness=10)
                return img_out, (x_pos, y_pos, radius)
        return frame, None
        
    def get_frame(self):
        # 返回array数组
        self.last_access = time.time()
        self.initialize()
        return self.transform(self.frame)

    def _thread(self):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.rotation = 180
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = PiRGBArray(camera)
            for foo in camera.capture_continuous(stream, 'bgr',
                                                 use_video_port=True):
                self.frame = stream.array
                stream.truncate(0)
                if time.time() - self.last_access > 10:
                    break
            
        self.thread = None

if __name__ == "__main__":
    c = Camera()
    while True:
        # print(c.thread)
        data = c.get_frame()
    # print(type(data))
    
