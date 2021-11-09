# based on github.com/lesp/electromaker-RCWL-0516

from gpiozero import DigitalInputDevice
from time import sleep
import datetime

radar = DigitalInputDevice(17, pull_up=False, bounce_time=2.0)

def detector():
    timestamp = str(datetime.datetime.now())
    print("Object detected at {}".format(timestamp))


print("Started object detection")
while True:
    radar.when_activated = detector
    sleep(2)
