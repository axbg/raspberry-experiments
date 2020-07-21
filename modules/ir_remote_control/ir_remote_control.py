# based on https://github.com/Lime-Parallelogram/IR-Code-Referencer

import RPi.GPIO as GPIO
from datetime import datetime


signal_pin = 11

buttons = [
    0x300ffa25d,
    0x300ff629d,
    0x300ffe21d,
    0x300ff22dd,
    0x300ff02fd,
    0x300ffc23d,
    0x300ffe01f,
    0x300ffa857,
    0x300ff906f,
    0x300ff6897,
    0x300ff9867,
    0x300ffb04f,
    0x300ff18e7,
    0x300ff38c7,
    0x300ff10ef,
    0x300ff5aa5,
    0x300ff4ab5,
]

buttons_names = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '*',
    '0',
    '#',
    'UP',
    'OK',
    'LEFT',
    'RIGHT',
    'DOWN',
]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(signal_pin, GPIO.IN)


def getBinary():
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


try:
    print("Waiting for input")
    print("Enter ### to close the program")

    close_symbol = 0

    while True:
        input_data = convert_hex(getBinary())

        for button in range(len(buttons)):
            if hex(buttons[button]) == input_data:
                print(buttons_names[button])

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
