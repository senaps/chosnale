import datetime
import os
from urllib.parse import quote
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import desc

# we will read the database_uri elements from os environment_variables and
# initiate a db_uri. this is being used to connect and add the data to the db.
# quote() is used to escape special charachters form `username` and `password`

username = quote(os.environ.get('username', 'root'), safe='')
password = quote(os.environ.get('password', ''), safe='')
database = os.environ.get('database', 'localhost')
db_name = os.environ.get('db_name', 'chosnale')
db_uri = f"mysql+pymysql://{username}:{password}@{database}/{db_name}"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

order_types = ['featured', 'votes', 'pub_date']  # order_by strings we accept

def get_order(obj, order):
    return getattr(obj, order)


class Chosnale(db.Model):
    __tablename__="chosnales"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(240))
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    featured = db.Column(db.Boolean, default=False)
    votes = db.Column(db.Integer, default=0)


@app.route("/")
@app.route("/chosnale/", methods=['GET'])
@app.route("/chosnale/<int:page>/", methods=['GET'])
@app.route("/chosnale/<int:page>/<int:per_page>/", methods=['GET'])
@app.route("/chosnale/<int:page>/<int:per_page>/<order>/", methods=['GET'])
def get_chosnale(page=1, per_page=10, order="pub_date"):
    """download chosnales from the db

    this function will receive some options such as `sorting value` or chosnale
    per page and will generate the result accordingly.
    we will use the pagination functionality of `sqlalchemy` to reduce the
    load on the db and amount the data we want to show.

    the only way to customize the data that is being received, one would need
    to send over a `POST` request.
    """
    status_code = 200
    chosnale_list = Chosnale.query.filter()  #query_all
    if chosnale_list:
        if order and order in order_types:  # order_by
            order = get_order(Chosnale, order)
            chosnale_list = chosnale_list.order_by(desc(order))
        else:
            chosnale_list = chosnale_list.order_by(desc(Chosnale.pub_date))
        chosnale_list = chosnale_list.paginate(page=page,
                                               per_page=per_page,
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
        status_code = 204
        response = {"result": "no data in the db!"}
    return jsonify(response), status_code

@app.route("/chosnale/", methods=['POST'])
def add_chosnale():
    """add a new chosnale

    this function will receive some text with at-most `240` charachters and
    will save it to the database, no actions performed on it.

    """
    data = request.get_json()
    chosnale_str = data.get('chosnale')
    if chosnale_str:
        if len(chosnale_str) > 240:
            response = {"result": "your chosnale should be 240 chars long"}
            status_code = 203
        else:
            chosnale = Chosnale(text=chosnale_str)
            db.session.add(chosnale)
            db.session.commit()
            response = {"result": "chosnale saved successfully"}
            status_code = 201
    else:
        response = {"result": "you should provide a `chosnale` field."}
        status_code = 400
    return jsonify(response), status_code


@app.route("/chosnale/vote/<int:id>/")
def vote(id=None):
    """cast a vote on a chosnale

    this function will check if a chosnale with provided `id` is present, and
    will add `1` votes to it's votes count. currently it wont do anything, but
    later on, we can manage to send featured chosnale's(ones with most votes) to
    twitter!

    :param id: the id of the chosnale we want to cast our vote for! :)
    """
    if id is None:
        response = {"result": "id should be a valid integer"}
        status_code = 400
    else:
        chosnale = Chosnale.query.filter_by(id=id).first()
        if chosnale:
            chosnale.votes += 1
            db.session.commit()
            response = {"result": "successfully voted up!"}
            status_code = 201
        else:
            response = {"result": "didn't find this chosnale"}
            status_code = 203
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)