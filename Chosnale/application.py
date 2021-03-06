from flask import Flask

from .extensions import db


def create_app(**kwargs):
    app = Flask(__name__)
    load_configs(app=app, **kwargs)
    load_blueprints(app)
    db.init_app(app)
    db.create_all(app=app)

    return app


def load_configs(app, **kwargs):
    app.config['SQLALCHEMY_DATABASE_URI'] = kwargs.get('db_uri')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if 'testing' in kwargs.keys():
        app.config['TESTING'] = True
    if 'debug' in kwargs.keys():
        app.config['DEBUG'] = True
    return app


def load_blueprints(app):
    from .apps import chosnale

    app.register_blueprint(chosnale)
