import pytest

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
