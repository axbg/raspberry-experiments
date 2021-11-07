# inspired by https://www.youtube.com/watch?v=Qq9svChQ5Do

import RPi.GPIO as GPIO
import time

GPIO_PIN = 26
PAUSE_DURATION = 0.5

GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_PIN, GPIO.OUT, 1)

while True:
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(PAUSE_DURATION)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(PAUSE_DURATION)
