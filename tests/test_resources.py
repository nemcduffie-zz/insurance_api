from flask import json


def test_token_access(app, client) -> None:
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
