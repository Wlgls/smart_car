#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File			:object_detect.py
@Time			:2020/08/29 15:51:40
@Author			:wlgls
@Version		:1.0
@Abstract       :使用tensorflow进行物品识别。
'''

import threading
import time
import cv2
import numpy as np
import os
import sys
import socket
import struct
from picamera.array import PiRGBArray
from picamera import PiCamera

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_utils

sys.path.append(os.getcwd()+"/utils")
class object_Detect(object):
    
    HOST = '192.168.1.102'  # ip of PC
    PORT = 8000  # 随便设置一个，对应起来就行
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.connect((HOST,PORT))

    # 初始线程配置
    Thread = None
    frame = None
    last_access = 0

    # 将视频存在本地
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_out = cv2.VideoWriter('out.mp4', fourcc, 2, (640, 480))

    # 模型配置
    print("loding--")
    CWD_PATH = os.path.join(os.getcwd(), 'utils')
    MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'  
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME , 'frozen_inference_graph.pb')   
    PATH_TO_LABELS = os.path.join(CWD_PATH, 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90   
    if not os.path.isfile(PATH_TO_CKPT):
        print("Model does not exist")
        exit

    #　加载模型
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    categories_index = label_map_util.create_category_index(categories)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') 
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0') 
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0') 
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0') 
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    
    def run(self):
        print("测试：",object_Detect.Thread)
        if object_Detect.Thread is None:
            print("new thread")
            object_Detect.Thread = threading.Thread(target=self._thread)
            object_Detect.Thread.start()
            print(object_Detect.Thread)
            while object_Detect.frame is None:
                time.sleep(0)

    """ def object_det(self):
        t_start = time.time()
        with self.detection_graph.as_default():
            with tf.compat.v1.Session(graph=self.detection_graph) as sess:
                self.frame.setflags(write=1)
                image_np_expanded = np.expand_dims(self.frame, axis=0)
                print("Running detection")

                (boxes, scores, classes, num) = sess.run(
                    [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
                    feed_dict={self.image_tensor:image_np_expanded}
                )

                vis_utils.visualize_boxes_and_labels_on_image_array(
                    self.frame,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.categories_index,
                    use_normalized_coordinates=True,
                    line_thickness=8
                )
                self.video_out.write(self.frame)
                # self.VideoTransmission(self.frame)
        print(time.time()-t_start)
        return self.frame
        """
    def transform(self, frame):
        message = None
        success, imagecode = cv2.imencode(".jpeg", frame)
        return imagecode, message

    def get_frame(self):
        # 返回array数组
        object_Detect.last_access = time.time()
        print("run--")
        self.run()
        return self.transform(self.frame)

    def VideoTransmission(self, frame):
        
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])  #编码
        try:
            self.server.sendall(struct.pack('i',imgencode.shape[0]))  # 发送数据长度作为校验
            self.server.sendall(imgencode)
            print("have sent one frame")
        except:
            print("fail to send the frame")

    @classmethod
    def _thread(cls):
        with cls.detection_graph.as_default():
            with tf.compat.v1.Session(graph=cls.detection_graph) as sess:
                with PiCamera() as camera:
                    # camera setup
                    camera.resolution = (640, 480)
                    camera.rotation = 180
                    camera.hflip = True
                    camera.vflip = True

                    # let camera warm up
                    camera.start_preview()
                    time.sleep(2)

                    stream = PiRGBArray(camera)
                    for foo in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                        t_start = time.time()
                        frame = np.array(stream.array)
                        frame.setflags(write=1)
                        image_np_expanded = np.expand_dims(frame, axis=0)
                        print("Running detection")

                        (boxes, scores, classes, num) = sess.run(
                            [cls.detection_boxes, cls.detection_scores, cls.detection_classes, cls.num_detections],
                            feed_dict={cls.image_tensor:image_np_expanded}
                        )

                        vis_utils.visualize_boxes_and_labels_on_image_array(
                            frame,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            cls.categories_index,
                            use_normalized_coordinates=True,
                            line_thickness=8
                        )
                        cls.video_out.write(frame)
                        cls.frame = frame
                        stream.truncate(0)
                        mfpf = 1 /(time.time()-t_start)
                        # print(mfpf)
                        # time.sleep(2)
                        print(time.time())
                        print(cls.last_access)
                        if time.time() - cls.last_access > 200:
                            break 
        cls.Thread = None

if __name__ == "__main__":
    try:
        od = object_Detect()
        
        od.get_frame()
        print(od.Thread)
        time.sleep(2)
        print(object_Detect.Thread)
        od.get_frame()
        print("object")


    except KeyboardInterrupt:
        exit