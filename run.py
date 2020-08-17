from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from insurance_api.config import config_settings

def create_app(config_class='development'):
    app = Flask(__name__, root_path='insurance_api/')

    app.config.from_object(config_settings[config_class])

    jwt = JWTManager(app)
    api = Api(app)

    from insurance_api.resources import (Registration, Login, Logout, Secret)
    from insurance_api.models import db

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    api.add_resource(Registration, '/registration')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    # api.add_resource(TokenRefresh, '/token-refresh')
    api.add_resource(Secret, '/secret')
    
    from insurance_api.models import RevokedToken
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token) -> bool:
        jti = decrypted_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti)

    return app


app = create_app()



