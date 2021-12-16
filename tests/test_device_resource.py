
def test_get_device_no_match(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404


def test_put_new_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_put_same_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012345", "group": "Group Update" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_get_device(test_client):
    api = '/api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_post_device(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012346", "group": "Group name" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 201


def test_post_same_device(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012346", "group": "Group name" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 400


def test_get_all_devices(test_client):
    api = '/api/device'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_delete_device(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_delete_same_device(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_get_device_no_match_(test_client):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
