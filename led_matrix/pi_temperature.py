import RPi.GPIO as GPIO
from datetime import datetime
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
from time import sleep
import subprocess

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(1)
virtual = viewport(device, width=32, height=16)


def main():
    try:
        while True:
            temp = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).split("=")[1].split("'")[0]
            with canvas(virtual) as draw:
                text(draw, (4, 0), temp, fill="white", font=proportional(CP437_FONT))
                sleep(0.5)
    except Exception:
        GPIO.cleanup()
    except KeyboardInterrupt:    
        pass
    
if __name__ == "__main__":
    main()
