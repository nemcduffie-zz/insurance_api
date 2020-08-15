import os

class Config():
    DEBUG = True if os.getenv('DEBUG') == 'True' else False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_settings = {
    'development': Config
}
