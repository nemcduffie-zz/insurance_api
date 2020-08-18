from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, get_raw_jwt)
from sqlalchemy import exc
from typing import Dict, Tuple
from marshmallow import Schema, fields, validate

from insurance_api.models import User, RevokedToken
from insurance_api.insurance_recs import insurance_recs


class RegistrationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class Registration(Resource):
    def post(self) -> Tuple[Dict, int]:
        schema = RegistrationSchema()
        data = schema.dump(request.get_json())
        
        if User.find_user(data['username']):
            return {
                'message': 'User {} already exists'.format(data['username'])
            }, 422
        
        new_user = User(
            username = data['username'],
            password = User.pw_hash(data['password'])
        )
        
        try:
            new_user.save()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was successfully created'.format(
                    data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        except exc.SQLAlchemyError:
            return {'message': 'User wasn\'t able to be added to db'}, 500


class Login(Resource):
    def post(self) -> Tuple[Dict, int]:
        schema = RegistrationSchema()
        data = schema.dump(request.get_json())
        user = User.find_user(data['username'])

        if user and User.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 422


class Logout(Resource):
    @jwt_required
    def post(self) -> Tuple[Dict, int]:
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


def occupation_validator(value):
    if value not in ['Employed', 'Student', 'Self-employed']:
        raise ValueError 
    return x


class QuestionaireSchema(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    num_children = fields.Integer(required=True)
    occupation = fields.String(required=True)
    occupation_type = fields.String(required=True,
        validate=validate.OneOf(['Employed', 'Student', 'Self-employed']))
    email = fields.Email(required=True)


class Questionaire(Resource):
    @jwt_required
    def post(self) -> Tuple[Dict, int]:
        schema = QuestionaireSchema()
        data = schema.dump(request.get_json())

        username = get_jwt_identity()
        user = User.find_user(username)
        if not user:
            return {'message': 'Wrong credentials'}, 422

        for field in data.keys():
            setattr(user, field, data[field])
        user.children = True if user.num_children > 0 else False
        user.save()

        return {
            'message': 'User {} was successfully updated'.format(username),
            'recommendations': insurance_recs(user)
        }, 200

    @jwt_required
    def get(self) -> Tuple[Dict, int]:
        username = get_jwt_identity()
        user = User.find_user(username)
        if not user:
            return {'message': 'Wrong credentials'}, 422
        if not user.name:
            return {'message': 'Please fill in your user infromation'}, 422
        return {
            'message': 'User\'s recommendations successfully collected',
            'recommendations': insurance_recs(user)
        }, 200


class Secret(Resource):
    @jwt_required
    def get(self) -> Tuple[Dict, int]:
        return {
            'answer': 42
        }, 200
