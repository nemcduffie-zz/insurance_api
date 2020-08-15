from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config_settings

app = Flask(__name__)
api = Api(app)


app.config.from_object(config_settings['development'])

db = SQLAlchemy(app)
migrate.init_app(app, db)

