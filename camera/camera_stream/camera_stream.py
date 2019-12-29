import io
import cv2
import numpy as np
import socketserver

from threading import Condition, Thread
from http import server

PAGE="""\
<html>
<head>
<title>Live Cam</title>
</head>
<body>
<center><h1>Live Cam</h1></center>
<center><img src="stream.mjpg" width="1920" height="1080"></center>
</body>
</html>
"""

class StreamingOutput:
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, frame):
        with self.condition:
            formatted_frame = cv2.imencode(".jpg", frame)[1].tostring()
            self.frame = formatted_frame
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        #print(frame)
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    

def receive_feed(cap, output):
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        output.write(frame)


def main():
    cap = cv2.VideoCapture(0)
    output = StreamingOutput()
    try:
        thread = Thread(target = receive_feed, args = (cap, output))
        thread.start()
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    except:
        pass
    cap.release()


if __name__ == "__main__":
    main()
