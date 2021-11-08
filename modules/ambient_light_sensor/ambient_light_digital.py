# the TEMT6000 ambient light sensor is digital
#   it can be connected to a GPIO directly, though
#   it detect smooth transitions between light levels, 
#   but it can detect when the light level exceeds a threshold
# as explained on https://forums.raspberrypi.com/viewtopic.php?t=266525

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN)

while True:
    print (GPIO.input(26))
    time.sleep (1)
