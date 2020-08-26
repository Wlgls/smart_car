#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#  
#  
#  
import time
import io
import threading
import picamera
import os
from picamera.array import PiRGBArray
import cv2


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
                
    def transform(self, frame):
        success, imagecode = cv2.imencode(".jpeg", frame)
        return imagecode.tobytes()

    def get_frame(self):
        # 返回array数组
        Camera.last_access = time.time()
        self.initialize()
        _, imagecode = cv2.imencode(".jpeg", self.frame)
        return imagecode

    @classmethod
    def _thread(cls):
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
                cls.frame = stream.array
                stream.truncate(0)
                if time.time() - cls.last_access > 10:
                    break
            
        cls.thread = None

if __name__ == "__main__":
    c = Camera()
    data = c.get_frame()
    # print(type(data))
    
