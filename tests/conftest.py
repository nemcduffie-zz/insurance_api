import pytest

from flask_jwt_extended import create_access_token
from run import create_app
from insurance_api.models import db
from insurance_api.config import config_settings


@pytest.fixture(scope='session')
def app():
    ''' Fixture to test app.
    '''
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    ''' Fixture to test app api access.
    '''
    client = app.test_client()
    return client


@pytest.fixture(scope='function')
def headers(app, client):
    token = create_access_token(identity='test')
    headers = {'Authorization': 'Bearer {}'.format(token)}
    return headers
