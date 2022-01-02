
def test_get_group_no_match(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
    assert response.is_json is True


def test_put_new_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "url": "URL New", "name": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200
    assert response.is_json is True


def test_put_same_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "url": "URL Update", "name": "123456789012345" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 200
    assert response.is_json is True


def test_get_group(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_post_group(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 201
    assert response.is_json is True


def test_post_same_group(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 409
    assert response.is_json is True


def test_get_all_groups(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_delete_group(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_delete_same_group(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 200
    assert response.is_json is True


def test_get_groups_no_match_(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 404
    assert response.is_json is True


def test_get_all_group_no_bearer(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_get_group_no_bearer(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_put_group_no_bearer(test_client):
    api = '/api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client.put(api, headers=headers, data=body)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_post_group_no_bearer(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json'}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client.post(api, headers=headers, data=body)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_delete_group_no_bearer(test_client):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json'}
    response = test_client.delete(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header is expected"


def test_get_all_group_invalid_bearer_name(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': 'NoBearer 123'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header must be a Bearer token"


def test_get_all_group_invalid_bearer_one_part(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Token not found"


def test_get_all_group_invalid_bearer_three_parts(test_client):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer 123 Bearer'}
    response = test_client.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Authorization header must be a valid Bearer token"


def test_get_all_group_invalid_pub_key_in_token(test_client):
    import os
    pub_key = os.getenv("AUTH_PUBLIC_KEY")
    os.environ["AUTH_PUBLIC_KEY"] = "ABC"
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client.application.bearer}
    response = test_client.get(api, headers=headers)
    os.environ["AUTH_PUBLIC_KEY"] = pub_key
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Unable to parse authentication token"


def test_get_all_group_expired_token(test_client_expired_token):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_expired_token.application.bearer}
    response = test_client_expired_token.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Token is expired"


def test_get_all_group_missing_kid_in_token(test_client_missing_kid_in_token):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_missing_kid_in_token.application.bearer}
    response = test_client_missing_kid_in_token.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "No kid found in token"


def test_get_all_group_invalid_aud_in_token(test_client_invalid_aud_in_token):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_invalid_aud_in_token.application.bearer}
    response = test_client_invalid_aud_in_token.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "Incorrect claims, please check the audience and issuer"


def test_get_all_group_invalid_signature_in_token(test_client_invalid_signature_in_token):
    api = '/api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_invalid_signature_in_token.application.bearer}
    response = test_client_invalid_signature_in_token.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "The signature is not valid"


def test_get_all_group_missing_scope_in_token(test_client_missing_scope_in_token):
    api = '/api/group'
    headers = {'content-type': 'application/json',
               'Authorization': test_client_missing_scope_in_token.application.bearer}
    response = test_client_missing_scope_in_token.get(api, headers=headers)
    assert response.status_code == 401
    assert response.is_json is True
    assert response.json['description'] == "No matching scope found in token"
