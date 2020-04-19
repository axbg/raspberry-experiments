from threading import Thread

from flask import render_template, Response

from observer import Observer
from server import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(Observer.get_frame(), mimetype="multipart/x-mixed-replace; boundary=frame;")


if __name__ == '__main__':
    observer_thread = Thread(target=Observer.loop_detection)
    observer_thread.start()
    app.run()
