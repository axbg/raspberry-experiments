from datetime import datetime, timedelta
from threading import Lock, Thread

import os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

from database import Event, db
from server import app

MISSED_FRAME_COUNTER = 10


def save_event(start_timestamp, lost_timestamp):
    duration = (lost_timestamp - start_timestamp).total_seconds() / 60
    ev = Event(timestamp=start_timestamp, duration=duration)
    with app.app_context():
        db.session.add(ev)
        db.session.commit()


class Observer:
    colors = [(255, 255, 0) for x in range(80)]
    cam = cv2.VideoCapture(0)

    def __init__(self):
        self.frame = None
        self.lock = Lock()
        self.found = False
        self.found_timestamp = None
        self.lost_timestamp = None
        self.last_time_saved = None
        self.missed_frame = MISSED_FRAME_COUNTER

    def loop_detection(self):
        while True:
            self.detect()

    def detect(self):
        ret, im = Observer.cam.read()
        bbox, labels, conf = cv.detect_common_objects(im)
        if "cat" in labels:
            self.found = True
            self.missed_frame = MISSED_FRAME_COUNTER
            self.lost_timestamp = None
            if self.found_timestamp is None:
                self.found_timestamp = datetime.now()

            now = datetime.now()
            if self.last_time_saved is None or now > self.last_time_saved:
                self.last_time_saved = now + timedelta(minutes = 5)
                image_path = str(now.timestamp()) + ".jpg"
                cv2.imwrite(os.path.join(os.getcwd(), 'cat', image_path), im)

            im = draw_bbox(img=im, bbox=bbox, confidence=conf, labels=labels, colors=Observer.colors)
        elif self.found:
            if self.missed_frame > 0:
                if self.lost_timestamp is None:
                    self.lost_timestamp = datetime.now()

                self.missed_frame -= 1
            else:
                Thread(target=save_event, args=[self.found_timestamp, self.lost_timestamp]).start()

                self.found = False
                self.found_timestamp = None

        with self.lock:
            self.frame = im

    def get_frame(self):
        while True:
            with self.lock:
                _, encoded_image = cv2.imencode(".jpg", self.frame)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
