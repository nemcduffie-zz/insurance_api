from flask_restful import Resource, reqparse
from models import User, RevokedToken
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if User.find_user(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
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
                }
        except:
            return {'message': 'User wasn\'t able to be added to db.'}, 500

