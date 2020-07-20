# based on https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/

from datetime import datetime

import Adafruit_DHT
import time


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
ERR_COUNTER_LIMIT = 5

err_counter = 0
while True:
    hum, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    if hum is not None and temp is not None:
        err_counter = 0
        print("TEMP={}C HUM={}% ({})".format(temp, hum, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif err_counter == ERR_COUNTER_LIMIT:
        print("Sensor failed multiple times. Check wiring")
        exit(-1)
    else:
        err_counter += 1
    
    time.sleep(2)
    
