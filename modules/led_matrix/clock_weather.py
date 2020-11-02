import RPi.GPIO as GPIO

from time import sleep
from json import loads
from requests import get
from datetime import datetime
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.interface.serial import spi, noop
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

# EN/RO
language = "RO"
city = "Medgidia"

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(0)
virtual = viewport(device, width=32, height=16)
url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=16ec1bd19903f60a4cebefe29785a82c&units=metric".format(city)

def translate_weather(weather):
    up = weather.upper()
    
    if up == "CLEAR SKY":
        return "Cer senin"
    elif up == "LIGHT RAIN":
        return "Ploaie usoara"
    elif up == "FEW CLOUDS":
        return "Usor innorat"
    elif up == "SCATTERED CLOUDS" or up == "BROKEN CLOUDS":
        return "Nori risipiti"
    elif up == "CLOUDS":
        return "Innorat"    
    elif up == "Shower rain":
        return "Ploaie puternica"
    elif up == "RAIN":
        return "Ploaie"
    elif up == "THUNDERSTORM":
        return "Furtuna"
    elif up == "SNOW":
        return "Ninsoare"
    elif up == "MIST":
        return "Ceata"
    elif up == "DRIZZLE":
        return "Burnita"    
    else:
        return weather


def get_weather():
    parsed_response = loads(get(url).text)
    
    city = parsed_response["name"]
    temp = parsed_response["main"]["temp"]
    feels_like = parsed_response["main"]["feels_like"]
    weather = parsed_response["weather"][0]["description"].capitalize()    

    return [city, temp, feels_like, weather]

def format_minute(minute):
    if minute < 10:
        return "0{}".format(str(minute))
    return str(minute)

def format_temperature_offset(temp):
    if temp < 10:
        return 8
    return 3

def loop_time_and_temperature(temp, feels_like):
    rounded_temp = str(int(temp))
    rounded_feels_like = str(int(feels_like))
    feels_like_message = "Se simt ca" if language =="RO" else "Feels like"

    index = 0
    
    while index < 20:
        index += 1
        with canvas(virtual) as draw:
            current_time = datetime.now()
            offset = 4
            if current_time.hour > 9:
                offset = 1
            text(draw, (offset, 0), "{}:{}".format(str(current_time.hour), format_minute(current_time.minute)), fill="white", font=proportional(CP437_FONT))
        sleep(5) 
        with canvas(virtual) as draw:
            text(draw, (format_temperature_offset(temp), 0), "{}`C".format(rounded_temp), fill="white", font=proportional(CP437_FONT))
        sleep(5)
        show_message(device, "{} {}`C".format(feels_like_message, rounded_feels_like), fill="white", font=proportional(LCD_FONT), scroll_delay=0.04)    
          
def main():
    try:
        while True:
            [city, temp, feels_like, weather] = get_weather()
            translated_weather = translate_weather(weather) if language == "RO" else weather
            
            show_message(device, city, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
            show_message(device, translated_weather, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
                  
            loop_time_and_temperature(temp, feels_like)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
