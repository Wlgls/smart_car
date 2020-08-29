#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:object_detect.py
@Time			:2020/08/29 15:51:40
@Author			:wlgls
@Version		:1.0
@Abstract       :使用tensorflow进行物品识别。
'''

from camera_pi import Camera
import time
import cv2
import numpy as np
import os
from picamera.array import PiRGBArray
from picamera import PiCamera

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_utils

class Object_Detect(Camera):
    def __init__(self):
        # self.
        pass