from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config_settings

app = Flask(__name__)
api = Api(app)

# database.init_app(app)

app.config.from_object(config_settings['development'])

db = SQLAlchemy(app)
migrate = Migrate()
migrate.init_app(app, db)

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
