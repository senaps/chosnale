from flask import Flask, request, jsonify
from sqlalchemy import desc

from Chosnale.apps.chosnale import chosnale
from Chosnale.extensions import db
from .models import Chosnale
from .utils import get_order, order_types


@chosnale.route("/")
@chosnale.route("/chosnale/", methods=['GET'])
def get_chosnale():
    """download chosnales from the db

    this function will receive some options such as `sorting value` or chosnale
    per page and will generate the result accordingly.
    we will use the pagination functionality of `sqlalchemy` to reduce the
    load on the db and amount the data we want to show.

    the only way to customize the data that is being received, one would need
    to send over url arguments such as `page`, `per_page` and `order` in the
     url of the request.
    """
    data = request.args
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    order = data.get('order', 'pub_date')
    status_code = 200
    chosnale_list = Chosnale.query.filter()  #query_all
    if order and order in order_types:  # order_by
        order = get_order(Chosnale, order)
        chosnale_list = chosnale_list.order_by(desc(order))
    else:
        chosnale_list = chosnale_list.order_by(desc(Chosnale.pub_date))
    chosnale_list = chosnale_list.paginate(page=int(page),
                                           per_page=int(per_page),
                                           error_out=False
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
    return jsonify(response), status_code


@chosnale.route("/chosnale/", methods=['POST'])
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
            status_code = 400
        elif len(chosnale_str) < 15:
            response = {"result": "your chosnale should be atleast 15 chars long"}
            status_code = 400
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


@chosnale.route("/chosnale/vote/<int:id>/")
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
