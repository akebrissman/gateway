
def test_get_all_fb(test_client_no_db):
    api = 'api/firebase'
    headers = {'content-type': 'application/json'}
    response = test_client_no_db.get(api, headers=headers)
    assert response.status_code == 500


def test_put_fb_db_error(test_client_no_db):
    api = 'api/firebase/123456789012345'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token 30", "imsi": "123456789012346" }'
    response = test_client_no_db.put(api, headers=headers, data=body)
    assert response.status_code == 500


def test_post_fb_db_error(test_client_no_db):
    api = 'api/firebase'
    headers = {'content-type': 'application/json'}
    body = '{ "token": "Token 30", "imsi": "123456789012346" }'
    response = test_client_no_db.post(api, headers=headers, data=body)
    assert response.status_code == 500


def test_get_all_device(test_client_no_db):
    api = 'api/device'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    response = test_client_no_db.get(api, headers=headers)
    assert response.status_code == 500


def test_put_device_db_error(test_client_no_db):
    api = 'api/device/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client_no_db.put(api, headers=headers, data=body)
    assert response.status_code == 500


def test_post_device_db_error(test_client_no_db):
    api = 'api/device'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    body = '{ "name": "123456789012345", "group": "Group New" }'
    response = test_client_no_db.post(api, headers=headers, data=body)
    assert response.status_code == 500


def test_get_all_group(test_client_no_db):
    api = 'api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    response = test_client_no_db.get(api, headers=headers)
    assert response.status_code == 500


def test_put_group_db_error(test_client_no_db):
    api = 'api/group/123456789012345'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client_no_db.put(api, headers=headers, data=body)
    assert response.status_code == 500


def test_post_group_db_error(test_client_no_db):
    api = 'api/group'
    headers = {'content-type': 'application/json', 'Authorization': test_client_no_db.application.bearer}
    body = '{ "url": "URL 30", "name": "123456789012346" }'
    response = test_client_no_db.post(api, headers=headers, data=body)
    assert response.status_code == 500
