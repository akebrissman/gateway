
def test_get_group_no_match(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404


def test_put_new_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "url": "URL New", "name": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_put_same_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "url": "URL Update", "name": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_get_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_post_group(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json'}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 201


def test_post_same_group(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json'}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 400


def test_get_all_groups(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_delete_group(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_delete_same_group(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_get_group_no_match_(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
