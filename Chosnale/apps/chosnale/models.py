import datetime

from Chosnale.extensions import db


class Chosnale(db.Model):
    __tablename__="chosnales"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(240))
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    featured = db.Column(db.Boolean, default=False)
    votes = db.Column(db.Integer, default=0)

