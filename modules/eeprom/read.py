# inspired by: https://forums.raspberrypi.com/viewtopic.php?t=215217
# using EEPROM AT24C256

import smbus
import time

bus = smbus.SMBus(1)
i2c_addr = 0x50 # obtained using the i2cdetect -l and i2cdetect -y 1 commands

read_bytes = 128 # the number of bytes that you want to read from the eeprom

# EEPROM initialization
# sets address pointer to address 0x00, offset 0x00
bus.write_i2c_block_data(i2c_addr, 0x00, [0x00])

for i in range(0, read_bytes):
    value = bus.read_byte(i2c_addr)

    print(f"Read value: {value}")
    
    time.sleep(0.01)

