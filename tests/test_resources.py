
from flask import json
import pytest

from run import create_app
from insurance_api.models import db
from insurance_api.config import config_settings


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


def test_resources(app, client) -> None:
    response = client.get(
        '/secret',
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401

    response = client.post(
        '/registration',
        data=json.dumps({'username': 'test',
                         'password': 'testpw'}),
        content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    response = client.post(
        '/login',
        data=json.dumps({'username': 'test',
                         'password': 'testpw'}),
        content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    token = data.get('access_token')
    assert token
    headers = {'Authorization': 'Bearer {}'.format(token)}

    response = client.get(
        '/secret',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data.get('answer') == 42

    response = client.post(
        '/logout',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    response = client.get(
        '/secret',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
