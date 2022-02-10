# inspired by http://www.piddlerintheroot.com/vibration-sensor/

import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        print("Movement detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, callback, bouncetime=100)  # when a vibration is detected execute the callback method

while True:
        time.sleep(1)
