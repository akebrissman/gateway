
def test_get_fb_no_match(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404


def test_put_new_fb(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token New", "imsi": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_put_same_fb(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token Update", "imsi": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200


def test_get_fb(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_post_fb(test_client):
    api = '/api/firebase'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token 30", "imsi": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 201


def test_post_same_fb(test_client):
    api = '/api/firebase'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token 30", "imsi": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 409


def test_get_all_fbs(test_client):
    api = '/api/firebase'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200


def test_delete_fb(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_delete_same_fb(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200


def test_get_fb_no_match_(test_client):
    api = '/api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
