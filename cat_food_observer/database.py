from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.TIMESTAMP)
    duration = db.Column(db.Integer)

    def to_json(self):
        return {"id": self.id,
                "timestamp": "{}-{}-{}#{}:{}".format(self.timestamp.day, self.timestamp.month, self.timestamp.year,
                                                     self.timestamp.hour,
                                                     self.timestamp.minute if self.timestamp.minute > 9
                                                     else "0" + str(self.timestamp.minute)),
                "duration": self.duration}
