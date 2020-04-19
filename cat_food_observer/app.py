import json
from threading import Thread
from time import sleep

from flask import render_template, Response

from database import Event
from observer import Observer
from server import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    event_data = [x.to_json() for x in Event.query.all()]
    return Response(json.dumps(event_data), mimetype="application/json")


@app.route("/stream")
def stream():
    observer_instance = app.config.get("OBSERVER_INSTANCE")
    return Response(observer_instance.get_frame(), mimetype="multipart/x-mixed-replace; boundary=frame;")


if __name__ == '__main__':
    observer = Observer()
    app.config["OBSERVER_INSTANCE"] = observer
    Thread(target=observer.loop_detection).start()
    sleep(5)
    app.run()
