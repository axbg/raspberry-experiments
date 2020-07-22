# based on https://github.com/Arijit1080/mpu6050-with-Raspberry-Pi

# before running the script you must install
# sudo apt-get install i2c-tools python-smbus

# to check if the sensor is correctly connected run
# sudo i2cdetect -y 1
# you should see 68 available

import time
from mpu6050 import mpu6050


i2c_connection = 0x68
mpu = mpu6050(i2c_connection)


while True:
    accelerometer_data = mpu.get_accel_data()
    print("Accelerometer")
    print("\\tX: {}".format(str(accelerometer_data['x'])))
    print("\\tY: {}".format(str(accelerometer_data['y'])))
    print("\\tZ\n: {}".format(str(accelerometer_data['z'])))

    gyroscope_data = mpu.get_gyro_data()
    print("Gyroscope")
    print("\\tX: {}".format(str(gyroscope_data['x'])))
    print("\\tY: {}".format(str(gyroscope_data['y'])))
    print("\\tZ: {}\n".format(str(gyroscope_data['z'])))
    print("-------------------------------")
    time.sleep(1)
