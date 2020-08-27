from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity, get_raw_jwt)
from sqlalchemy import exc
from typing import Dict, Tuple
from marshmallow import Schema, fields, validate, ValidationError

from insurance_api.models import User
from insurance_api.insurance_recs import insurance_recs


class RegistrationSchema(Schema):
    ''' Schema for the parsing of Registration and Login requests.
    '''
    username = fields.String(required=True)
    password = fields.String(required=True)


class Registration(Resource):
    ''' Resource for User registation, logs in the user automatically
        in the form of returning an access token.
    '''
    def post(self) -> Tuple[Dict, int]:
        schema = RegistrationSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'message': err.messages}, 401

        if User.find_user(data['username']):
            return {
                'message': 'User {} already exists'.format(data['username'])
            }, 422

        new_user = User(
            username=data['username'],
            password=User.pw_hash(data['password'])
        )

        try:
            new_user.save()
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'User {} was successfully created'.format(
                    data['username']),
                'access_token': access_token
            }, 200
        except exc.SQLAlchemyError:
            return {'message': 'User wasn\'t able to be added to db'}, 500


class Login(Resource):
    ''' Resource for User login for already registered users.
    '''
    def post(self) -> Tuple[Dict, int]:
        schema = RegistrationSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'message': err.messages}, 401
        user = User.find_user(data['username'])

        if user and User.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 422


class QuestionaireSchema(Schema):
    ''' Schema for the parsing of the Questionaire requests.
    '''
    name = fields.String(required=True)
    address = fields.String(required=True)
    num_children = fields.Integer(required=True)
    occupation = fields.String(required=True)
    occupation_type = fields.String(required=True,
                                    validate=validate.OneOf(['Employed',
                                                             'Student',
                                                             'Self-employed']))
    email = fields.Email(required=True)


class Questionaire(Resource):
    ''' Resource for handling of questionaire data,
        all methods require a valid token.
    '''
    @jwt_required
    def post(self) -> Tuple[Dict, int]:
        ''' POST request method that accepts and saves the user's
            questionaire data and returns the user's insurance
            reccomendations based on that saved data.
        '''
        schema = QuestionaireSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'message': err.messages}, 401

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
        ''' GET request method returns the user's insurance
            reccomendations based on thier questionaire data
            saved by the POST request.
        '''
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
    ''' Resource requiring valid token, used
        for testing and development.
    '''
    @jwt_required
    def get(self) -> Tuple[Dict, int]:
        return {
            'answer': 42
        }, 200
