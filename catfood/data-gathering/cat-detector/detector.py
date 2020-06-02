from datetime import datetime, timedelta
from threading import Thread

import os
import cv2
import numpy as np
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


class Detector:
    def __init__(self):
        self.found = False
        self.found_timestamp = None
        self.lost_timestamp = None
        self.last_time_saved = None
        self.missed_frame = MISSED_FRAME_COUNTER

    def detect(self, image):
        npimg = np.fromstring(image, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        _, labels, _ = cv.detect_common_objects(image)

        if "cat" in labels:
            self.found = True
            self.missed_frame = MISSED_FRAME_COUNTER
            self.lost_timestamp = None

            if self.found_timestamp is None:
                self.found_timestamp = datetime.now()

            now = datetime.now()
            if self.last_time_saved is None or now > self.last_time_saved:
                self.last_time_saved = now + timedelta(minutes = 5)
                cv2.imwrite(os.path.join(os.getcwd(), 'cat', str(now.timestamp()) + ".jpg"), image)
                print("Cat found at: {}". format(now))

        elif self.found:
            if self.missed_frame > 0:
                self.missed_frame -= 1

                if self.lost_timestamp is None:
                    self.lost_timestamp = datetime.now()
            else:
                Thread(target=save_event, args=[self.found_timestamp, self.lost_timestamp]).start()
                self.found = False
                self.found_timestamp = None
