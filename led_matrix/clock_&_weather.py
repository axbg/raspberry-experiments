import RPi.GPIO as GPIO

from time import sleep
from datetime import datetime
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
from requests import get
from json import loads

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(1)
virtual = viewport(device, width=32, height=16)
api_key = "<your OpenWeather api key there>"
city = "<your city>" #example: Bucharest
url = "http://api.openweathermap.org/data/2.5/weather?q="+ city +"&appid=" + api_key + "&units=metric"


def get_weather():
    parsed_response = loads(get(url).text)
            
    city = parsed_response["name"]
    temp = parsed_response["main"]["temp"]
    weather = parsed_response["weather"][0]["description"].capitalize()    

    return [city, temp, weather]


def loop_time_and_temperature(hour, minute, temp):
    index = 0
    while index < 7:
        index += 1
        with canvas(virtual) as draw:
            current_time = datetime.now()
            offset = 4
            if current_time.hour > 9:
                offset = 1
            text(draw, (offset, 0), str(current_time.hour) + ":" + str(current_time.minute), fill="white", font=proportional(CP437_FONT))
        sleep(5) 
        with canvas(virtual) as draw:
            text(draw, (3, 0), str(int(temp)) + "'C", fill="white", font=proportional(CP437_FONT))
        sleep(5)
            
          
def main():
    try:
        while True:
            [city, temp, weather] = get_weather()
            current_time = datetime.now()
            
            show_message(device, city, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
            show_message(device, weather, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
                  
            loop_time_and_temperature(current_time.hour, current_time.minute, temp)
    except Exception as e:
        GPIO.cleanup()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()