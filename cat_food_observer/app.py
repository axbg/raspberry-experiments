from flask import render_template
from datetime import datetime

from database import db, Event
from server import app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
