from gateway.models.firebase import FirebaseModel


def test_new_user():
    obj = FirebaseModel('123456789012345', 'guid')
    assert obj.imsi == '123456789012345'
    assert obj.token == 'guid'
    assert obj.__repr__() == f"FirebaseModel(imsi={obj.imsi}, token={obj.token})"
    assert obj.__str__() == f"Imsi:{obj.imsi}, Token:{obj.token}"
    assert str(obj) == f"Imsi:{obj.imsi}, Token:{obj.token}"
    assert obj.json() == {'imsi': '123456789012345', 'token': 'guid'}


def test_save_obj(app):
    imsi = '123456789012345'
    token = 'ABC123'
    obj1 = FirebaseModel(imsi, token)
    obj1.save_to_db()

    obj2 = FirebaseModel.find_by_imsi(imsi)

    assert obj1.imsi == obj2.imsi
    assert obj1.token == obj2.token

    for x in FirebaseModel.find_all():
        assert x.imsi == imsi


def test_save_obj_mulitple_times(app):
    imsi = '123456789012345'
    token = 'ABC123'
    obj1 = FirebaseModel(imsi, token)
    obj1.save_to_db()
    obj1.save_to_db()
    obj1.save_to_db()
    assert len(FirebaseModel.find_all()) == 1


def test_delete_obj(app):
    imsi = '123456789012345'
    token = 'ABC123'
    obj1 = FirebaseModel(imsi, token)
    obj1.save_to_db()
    assert len(FirebaseModel.find_all()) == 1

    obj1.delete_from_db()
    assert len(FirebaseModel.find_all()) == 0


def test_find_obj(app):
    imsi = '123456789012345'
    token = 'ABC123'
    obj1 = FirebaseModel(imsi, token)
    obj1.save_to_db()

    obj2 = FirebaseModel.find_by_imsi("")
    assert obj2 is None

    obj2 = FirebaseModel.find_by_imsi(imsi)
    assert obj2 is not None
