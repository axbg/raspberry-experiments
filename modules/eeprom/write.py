# inspired by: https://forums.raspberrypi.com/viewtopic.php?t=215217
# using EEPROM AT24C256

import smbus
import time

bus = smbus.SMBus(1)
i2c_addr = 0x50 # obtained using the i2cdetect -l and i2cdetect -y 1 commands

write_bytes = 128 # the number of bytes that will be written

data = 0x80  # the first value that will be written
start_address = 0x00 # the address where the data will be written
offset = 0x00 # the offset to the start_address

for i in range(0, write_bytes):
    bus.write_i2c_block_data(i2c_addr, start_address, [offset, data])

    print(f'Written: {data}, address: {start_address}, offset: {offset}')
   
    data += 1
    offset += 1
 
    time.sleep(0.01)

