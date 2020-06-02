from flask import Flask
from database import db
from os import path

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="template")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(path.join(path.dirname(__file__), "app.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
