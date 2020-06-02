from datetime import datetime
from time import sleep

import cv2
import requests 

class Observer:
    colors = [(255, 255, 0) for x in range(80)]
    cam = cv2.VideoCapture(0)

    def __init__(self):
        self.frame = None

    def capture(self):
        while True:
            ret, im = Observer.cam.read()
            self.frame = im
        
    def send_frame(self):
        while True:
            image = cv2.imencode(".jpg", self.frame)[1]
            data = image.tostring()
            headers = {'Content-Type': 'application/json'}
            r = requests.post("http://192.168.0.144/", headers=headers, data=data)
            
    def get_frame(self):
        while True:
            _, encoded_image = cv2.imencode(".jpg", self.frame)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
