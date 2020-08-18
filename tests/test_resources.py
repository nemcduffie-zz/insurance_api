from flask import json
from tests.chuck_recs import CHUCK_RECS


def test_token_access(app, client) -> None:
    ''' Tests the User registration/login/logout flow.
    '''
    response = client.get(
        '/secret',
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    # Should fail because user is not registered
    assert response.status_code == 401

    response = client.post(
        '/registration',
        data=json.dumps({'username': 'test',
                         'password': 'testpw'}),
        content_type='application/json')
    # Registration should be successful
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    response = client.post(
        '/login',
        data=json.dumps({'username': 'test',
                         'password': 'testpw'}),
        content_type='application/json')
    # Login should be successful, add token to headers
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
    # Should be allowed to access the secret 42
    assert response.status_code == 200
    assert data.get('answer') == 42

    response = client.post(
        '/logout',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    # Should successfully logout, token should now be invalid
    assert response.status_code == 200

    response = client.get(
        '/secret',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    # Secret should now fail since token is invalid
    assert response.status_code == 401


def test_questionaire(app, client) -> None:
    ''' Tests the Questionaire Resource that returns insurance options.
    '''
    response = client.post(
        '/login',
        data=json.dumps({'username': 'test',
                         'password': 'testpw'}),
        content_type='application/json')
    # Login should be successful, add token to headers
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    token = data.get('access_token')
    assert token
    headers = {'Authorization': 'Bearer {}'.format(token)}

    user_info = {  # Test data
        'name': 'Chuck',
        'address': '15774 Longwood Dr. Los Gatos CA 95032',
        'num_children': 1,
        'occupation': 'Python Developer',
        'occupation_type': 'Employed',
        'email': 'chuck@chuck.com'
    }
    response = client.post(
        '/questionaire',
        headers=headers,
        data=json.dumps(user_info),
        content_type='application/json')
    # Request should save the user data and match our test json
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data.get('recommendations') == CHUCK_RECS

    response = client.get(
        '/questionaire',
        headers=headers,
        content_type='application/json')
    # Get request of already saved data should also match test json
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data.get('recommendations') == CHUCK_RECS

    response = client.post(
        '/logout',
        headers=headers,
        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    # Should successfully logout
    assert response.status_code == 200
