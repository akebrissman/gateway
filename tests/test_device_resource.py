
def test_get_device_no_match(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
    assert response.is_json is True


def test_put_new_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200
    assert response.is_json is True


def test_put_same_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "name": "123456789012345", "group": "Group Update" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200
    assert response.is_json is True


def test_get_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_post_device(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "name": "123456789012346", "group": "Group name" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 201
    assert response.is_json is True


def test_post_same_device(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "name": "123456789012346", "group": "Group name" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 409
    assert response.is_json is True


def test_get_all_devices(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_delete_device(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_delete_same_device(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_get_device_no_match_(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
    assert response.is_json is True


def test_get_all_devices_no_bearer(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_get_device_no_bearer(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_put_device_no_bearer(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_post_device_no_bearer(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012346", "group": "Group name" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_delete_device_no_bearer(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_get_all_devices_invalid_bearer_name(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json', 'Authorization': 'NoBearer 123'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header must be a Bearer token"


def test_get_all_devices_invalid_bearer_one_part(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Token not found"
