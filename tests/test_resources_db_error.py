
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
