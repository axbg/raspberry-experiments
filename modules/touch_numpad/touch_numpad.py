# based on https://github.com/083chandan/ttp229-pi

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SCLPin = 17
GPIO.setup(SCLPin, GPIO.OUT)

SDOPin = 4
GPIO.setup(SDOPin, GPIO.IN)

input_keys = 17
key_pressed = 0

def getKey():
    global key_pressed
    
    button = 0
    key_state = 0
 
    time.sleep(0.05)

    for i in range(input_keys):
        GPIO.output(SCLPin, GPIO.LOW)
        
        if not GPIO.input(SDOPin):
            key_state = i+1

        GPIO.output(SCLPin, GPIO.HIGH)

    if key_state > 0 and key_state != key_pressed:
        if key_state == 17:
            button = 1
        else:
            button = key_state
    
    key_pressed = key_state

    return button

try:
    print("Waiting for input")

    while True:
        key = getKey()

        if key > 0:
            print(key)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
