from flask import Flask

from .extensions import db


def create_app(configs):
    app = Flask(__name__)
    load_configs(app=app, config=configs)
    load_blueprints(app)
    db.init_app(app)

    return app


def load_configs(app, config):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db_uri')
    return app


def load_blueprints(app):
    from .apps import chosnale

    app.register_blueprint(chosnale)