import socket
import time
import imagezmq
from imutils.video import VideoStream

sender = imagezmq.ImageSender(connect_to="tcp://localhost:5555")

rpi_name = "pc"
cam = VideoStream(0).start()
time.sleep(2.0)
while True:
	image = cam.read()
	sender.send_image(rpi_name, image)