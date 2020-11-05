import RPi.GPIO as GPIO

from constants import buttons, buttons_names

from datetime import datetime
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.interface.serial import spi, noop
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT


def getBinary(signal_pin):
    consecutive_ones = 0
    binary = 1
    command = []
    previous_value = 0
    
    value = GPIO.input(signal_pin)
    while value:
        value = GPIO.input(signal_pin)

    startTime = datetime.now()
    while True:
        if previous_value != value:
            now = datetime.now()
            pulse_time = now - startTime
            startTime = now
            
            if previous_value:
                command.append((previous_value, pulse_time.microseconds))

        if value:
            consecutive_ones += 1
        else:
            consecutive_ones = 0

        if consecutive_ones > 10000:
            break

        previous_value = value
        value = GPIO.input(signal_pin)

    for (_, duration) in command:
        if duration > 1000:
            binary = binary * 10 + 1
        else:
            binary *= 10

    if len(str(binary)) > 34:
        binary = int(str(binary)[:34])

    return binary


def convert_hex(binary_value):
    return hex(int(str(binary_value), 2))


def handle_input(device, number):
    show_message(device, "Hello {}".format(number), fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)


try:
    # initialize IR receiver
    signal_pin = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(signal_pin, GPIO.IN)
    
    # initialize matrix
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=32, height=8, block_orientation=-90)
    device.contrast(0)
    virtual = viewport(device, width=32, height=16)

    print("Waiting for input")
    print("Enter ### to close the program")

    close_symbol = 0

    while True:
        input_data = convert_hex(getBinary(signal_pin))

        for button in range(len(buttons)):
            if hex(buttons[button]) == input_data:
                handle_input(device, buttons_names[button])

                if buttons_names[button] == '#':
                    if close_symbol == 2:
                        print("Exiting")
                        exit(0)
                    else:
                        close_symbol += 1
                else:
                    close_symbol = 0
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
