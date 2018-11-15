import datetime
import os
from urllib.parse import quote
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import desc

username = quote(os.environ.get('username', 'root'), safe='')
password = quote(os.environ.get('password', ''), safe='')
database = os.environ.get('database', 'localhost')
db_name = os.environ.get('db_name', 'chosnale')
db_uri = f"mysql+pymysql://{username}:{password}@{database}/{db_name}"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
db.create_all()
order_types = ['featured', 'votes', 'pub_date']


class Chosnale(db.Model):
    __tablename__="chosnales"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(240))
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    featured = db.Column(db.Boolean, default=False)
    votes = db.Column(db.Integer, default=0)


@app.route("/get_chosnale/", methods=['GET','POST'])
def get_chosnale():
    data = request.get_json() or {}
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    chosnale_order = data.get('order')
    status_code = 200
    chosnale_list = Chosnale.query.filter()  #query_all
    if chosnale_list:
        if chosnale_order and chosnale_order in order_types:  # order_by
            order = get_chosnale(Chosnale, chosnale_order)
            chosnale_list = chosnale_list.order_by(desc(order))
        else:
            chosnale_list = chosnale_list.order_by(desc(Chosnale.pub_date))
        chosnale_list = chosnale_list.paginate(page=page,
                                               per_page=per_page
                                               )
        results_list = list()
        for chosnale in chosnale_list.items:
            obj = dict()
            obj['id'] = chosnale.id
            obj['text'] = chosnale.text
            obj['pub_date'] = chosnale.pub_date
            obj['featured'] = chosnale.featured
            obj['votes'] = chosnale.votes
            results_list.append(obj)
        response = {"result": {
            "data": results_list,
            "page": page,
            "per_page": per_page,
            }}
        status_code = 200
    else:
        status_code = 201
        response = {"result": "no data in the db!"}
    return jsonify(response), status_code


@app.route("/add_chosnale/", methods=['POST'])
def add_chosnale():
    data = request.get_json()
    chosnale_str = data.get('chosnale')
    if len(chosnale_str) > 240:
        response = {"result": "your chosnale should be 240 chars long"}
        status_code = 201
    else:
        chosnale = Chosnale(text=chosnale_str)
        db.session.add(chosnale)
        db.session.commit()
        response = {"result": "chosnale saved successfully"}
        status_code = 200
    return jsonify(response), status_code


@app.route("/vote/<int:id>/")
def vote(id=None):
    if id is None:
        response = {"result": "id should be a valid integer"}
        status_code = 300
    else:
        chosnale = Chosnale.query.filter_by(id=id).first()
        if chosnale:
            chosnale.votes += 1
            db.session.commit()
            response = {"result": "successfully voted up!"}
            status_code = 200
        else:
            response = {"result": "didn't find this chosnale"}
            status_code = 201
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run()