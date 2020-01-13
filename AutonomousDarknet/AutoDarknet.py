from ctypes import *
# import math
# import random
import os
import cv2
# import numpy as np
# import time
# import AutonomousDarknet.darknet as darknet # TODO: Uncomment when using Autonomous

netMain = None
metaMain = None
altNames = None
counter = 0
conf_list = []

objects = ["left_arrow", "right_arrow", "tennis_ball", "NULL"]
frames_taken = 40


def calc_conf(inp_list):
    result = [inp_list.count(obj)/frames_taken for obj in objects]
    return result


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img


'''
class AutoDarknet:
    def __init__(self,cameraDeviceNumber=0):
        global metaMain, netMain, altNames
        self.object_detected = "Null"
        configPath = "./AutonomousDarknet/yolo-obj.cfg"
        weightPath = "./AutonomousDarknet/yolo-obj_final.weights"
        metaPath = "./AutonomousDarknet/obj.data"
        self.threshold = 0.6
        if not os.path.exists(configPath):
            raise ValueError("Invalid config path `" +
                             os.path.abspath(configPath)+"`")
        if not os.path.exists(weightPath):
            raise ValueError("Invalid weight path `" +
                             os.path.abspath(weightPath)+"`")
        if not os.path.exists(metaPath):
            raise ValueError("Invalid data file path `" +
                             os.path.abspath(metaPath)+"`")
        if netMain is None:
            netMain = darknet.load_net_custom(configPath.encode(
                "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        if metaMain is None:
            metaMain = darknet.load_meta(metaPath.encode("ascii"))
        if altNames is None:
            try:
                with open(metaPath) as metaFH:
                    metaContents = metaFH.read()
                    import re
                    match = re.search("names *= *(.*)$", metaContents,
                                      re.IGNORECASE | re.MULTILINE)
                    if match:
                        result = match.group(1)
                    else:
                        result = None
                    try:
                        if os.path.exists(result):
                            with open(result) as namesFH:
                                namesList = namesFH.read().strip().split("\n")
                                altNames = [x.strip() for x in namesList]
                    except TypeError:
                        pass
            except Exception:
                pass
        self.cap = cv2.VideoCapture(cameraDeviceNumber)
        # self.cap.set(3, 1600)
        # self.cap.set(4, 900)
        self.out = cv2.VideoWriter(
            "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
            (darknet.network_width(netMain), darknet.network_height(netMain)))

        # Create an image we reuse for each detect
        self.darknet_image = darknet.make_image(
            darknet.network_width(netMain), darknet.network_height(netMain), 3)

        print("AutoDarknet object constructed!")  # Debugging

    def __del__(self):
        self.cap.release()
        self.out.release()
        print("AutoDarknet object destroyed!")  # Debugging

    def get_detected_obj(self, detections):
        global counter, conf_list, frames_taken, objects
        if len(detections) > 0:
            object_name = detections[0][0].decode()
            # print(object_name)
            if(object_name in objects):
                conf_list.append(object_name)

        else:
            conf_list.append("NULL")
        counter += 1
        if(counter == frames_taken):
            conf_result = calc_conf(conf_list)
            self.object_detected = objects[conf_result.index(max(conf_result))]
            print("-----------------------------------")
            print("Confidence values calculated for : ", frames_taken)
            print("Confidence Value for left_arrow is : ", conf_result[0])
            print("Confidence Value for right_arrow is :", conf_result[1])
            print("Confidence Value for tennis_ball is : ", conf_result[2])
            print("Confidence Value for NULL is : ", conf_result[3])
            print("-----------------------------------\n")

            counter = frames_taken - 1
            conf_list.pop(0)

    def get_frame(self):
        """Reads the frames from the Camera and returns the image with annotation,
        if object detected."""
        global metaMain, netMain, altNames
        ret, frame_read = self.cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(
            self.darknet_image, frame_resized.tobytes())

        detections = darknet.detect_image(  # Detect
            netMain, metaMain, self.darknet_image, thresh=self.threshold)

        self.get_detected_obj(detections)

        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        return image

    def get_frame_bytes(self):
        """Reads the frames from the get_frame and returns them jped in bytes."""
        image = self.get_frame()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def gen(self):
        """An infinite loop function to be passed in the Response section for the Feed"""
        while True:
            frame = self.get_frame_bytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
'''

class AutoDarknet:
    def __init__(self,cameraDeviceNumber=0):
        self.video = cv2.VideoCapture(cameraDeviceNumber)
        self.object_detected = "Null"
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def gen(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
