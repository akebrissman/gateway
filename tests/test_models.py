from gateway.models.firebase import FirebaseModel

def test_new_user(new_fb):
    fb = new_fb
    assert fb.imsi == '123456789012345'
    assert fb.token == 'guid'
    assert fb.__repr__() == f"FirebaseModel(imsi={fb.imsi}, token={fb.token})"
    assert fb.__str__() == f"Imsi:{fb.imsi}, Token:{fb.token}"
    assert str(fb) == f"Imsi:{fb.imsi}, Token:{fb.token}"

    assert str(fb.json()) == f"{{'imsi': '{fb.imsi}', 'token': '{fb.token}'}}"
    # should be this for valid json syntax.
    # assert new_fb.json() == f"{{\"imsi\": \"{new_fb.imsi}\", \"token\": \"{new_fb.token}\"}}"


def test_save_user(app):
    imsi = '123456789012345'
    token = 'ABC123'
    fb1 = FirebaseModel(imsi, token)
    fb1.save_to_db()

    fb2 = FirebaseModel.find_by_imsi(imsi)

    assert fb1.imsi == fb2.imsi
    assert fb1.token == fb2.token

    for x in FirebaseModel.find_all():
        assert x.imsi == imsi

def test_save_user_mulitple_times(app):
    imsi = '123456789012345'
    token = 'ABC123'
    fb1 = FirebaseModel(imsi, token)
    fb1.save_to_db()
    fb1.save_to_db()
    fb1.save_to_db()
    assert len(FirebaseModel.find_all()) == 1

def test_delete_user(app):
    imsi = '123456789012345'
    token = 'ABC123'
    fb1 = FirebaseModel(imsi, token)
    fb1.save_to_db()
    assert len(FirebaseModel.find_all()) == 1

    fb1.delete_from_db()
    assert len(FirebaseModel.find_all()) == 0

def test_find_user(app):
    imsi = '123456789012345'
    token = 'ABC123'
    fb1 = FirebaseModel(imsi, token)
    fb1.save_to_db()

    fb2 = FirebaseModel.find_by_imsi("")
    assert fb2 is None

    fb2 = FirebaseModel.find_by_imsi(imsi)
    assert fb2 is not None
