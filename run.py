#!/usr/bin/env python3.8

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from insurance_api.config import config_settings
from marshmallow import ValidationError


def create_app(config_class='development'):
    ''' Method to initalize app and it's api routes.
    '''
    app = Flask(__name__, root_path='insurance_api/')

    app.config.from_object(config_settings[config_class])

    jwt = JWTManager(app)
    api = Api(app)

    from insurance_api.resources import (Registration, Login,
                                         Questionaire, Secret)
    from insurance_api.models import db

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    api.add_resource(Registration, '/registration')
    api.add_resource(Login, '/login')
    api.add_resource(Questionaire, '/questionaire')
    api.add_resource(Secret, '/secret')

    @app.errorhandler(ValidationError)
    def handle_bad_request(e):
        return e.messages, 422

    return app


app = create_app()
