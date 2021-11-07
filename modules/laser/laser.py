# inspired by https://www.youtube.com/watch?v=Qq9svChQ5Do

import RPi.GPIO as GPIO
import time

def run_cycle(pin, pause_duration, cycles):
    ct = 0
    while ct < cycles:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(pause_duration)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(pause_duration)
        ct += 1


GPIO_PIN = 26
FIRST_PATTERN_CYCLE = 0.5
SECOND_PATTERN_CYCLE = 0.25

GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_PIN, GPIO.OUT)

while True:
    run_cycle(GPIO_PIN, 0.5, 2)
    run_cycle(GPIO_PIN, 0.25, 4)
    run_cycle(GPIO_PIN, 0.10, 8)
