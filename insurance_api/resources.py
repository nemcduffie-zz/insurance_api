from typing import Dict, Tuple
from flask_restful import Resource, reqparse
from flask_restplus import inputs
from insurance_api.models import User, RevokedToken
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, #jwt_refresh_required,
                                get_jwt_identity, get_raw_jwt)


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help ='This field cannot be blank', required=True)
user_parser.add_argument('password', help ='This field cannot be blank', required=True)


class Registration(Resource):
    def post(self) -> Tuple[Dict, int]:
        data = user_parser.parse_args()
        
        if User.find_user(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])} #TODO: status code
        
        new_user = User(
            username = data['username'],
            password = User.pw_hash(data['password'])
        )
        
        try:
            new_user.save()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was successfully created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        except:
            return {'message': 'User wasn\'t able to be added to db'}, 500


class Login(Resource):
    def post(self) -> Tuple[Dict, int]:
        data = user_parser.parse_args()
        curr_user = User.find_user(data['username'])

        if curr_user and User.verify_hash(data['password'], curr_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(curr_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        else:
            return {'message': 'Wrong credentials'}, 404


class Logout(Resource):
    @jwt_required
    def post(self) -> Tuple[Dict, int]:
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


# class TokenRefresh(Resource):
#     @jwt_refresh_required
#     def post(self) -> Tuple[Dict, int]:
#         curr_user = get_jwt_identity()
#         access_token = create_access_token(identity = curr_user)
#         return {'access_token': access_token}


class Secret(Resource):
    @jwt_required
    def get(self) -> Tuple[Dict, int]:
        return {
            'answer': 42
        }
