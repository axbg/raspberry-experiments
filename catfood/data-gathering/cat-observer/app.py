import json
from threading import Thread
from time import sleep

from flask import Flask, render_template, Response

from observer import Observer

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="template")

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

observer = Observer()
app.config["OBSERVER_INSTANCE"] = observer
Thread(target=observer.capture).start()
sleep(1)
Thread(target=observer.send_frame).start()
app.run()
