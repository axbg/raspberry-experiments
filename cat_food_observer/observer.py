from threading import Lock

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox


class Observer:
    frame = None
    colors = [(255, 255, 0) for x in range(80)]
    cam = cv2.VideoCapture(0)
    lock = Lock()

    @staticmethod
    def loop_detection():
        while True:
            Observer.detect()

    @staticmethod
    def detect():
        ret, im = Observer.cam.read()
        bbox, labels, conf = cv.detect_common_objects(im)

        if "cat" in labels:
            im = \
                draw_bbox(img=im, bbox=bbox, confidence=conf, labels=labels, colors=Observer.colors)

        with Observer.lock:
            Observer.frame = im

    @staticmethod
    def get_frame():
        while True:
            with Observer.lock:
                _, encoded_image = cv2.imencode(".jpg", Observer.frame)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
