from flask import request
from detector import Detector
from server import app

@app.route("/", methods = ['POST'])
def index():
    detector.detect(request.data)
    return "OK"

if __name__ == '__main__':
    detector = Detector()
    app.run()
