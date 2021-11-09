# inspired by https://www.mbtechworks.com/projects/pir-motion-sensor-with-raspberry-pi.html

import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

pir = 14
GPIO.setup(pir, GPIO.IN)

time.sleep(2)

try:
    while True:
        if GPIO.input(pir) == True:
            print("Motion detected!")
        else:
            print("No motion")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

