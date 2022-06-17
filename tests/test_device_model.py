from gateway.models.device import DeviceModel


def test_new():
    obj = DeviceModel('12345', '54321')
    assert obj.name == '12345'
    assert obj.group == '54321'
    assert obj.__repr__() == f"DeviceModel(name={obj.name}, group={obj.group})"
    assert obj.__str__() == f"name:{obj.name}, group:{obj.group}"
    assert str(obj) == f"name:{obj.name}, group:{obj.group}"
    assert obj.json() == {'name': obj.name, 'group': obj.group}


def test_save_fb(app):
    name = '123456789012345'
    group = 'ABC123'
    obj1 = DeviceModel(name, group)
    obj1.save_to_db()

    obj2 = DeviceModel.find_by_name(name)

    assert obj1.name == obj2.name
    assert obj1.group == obj2.group

    for x in DeviceModel.find_all():
        assert x.name == name


def test_save_mulitple_times(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = DeviceModel(name, group)
    obj.save_to_db()
    obj.save_to_db()
    obj.save_to_db()
    assert len(DeviceModel.find_all()) == 1


def test_delete(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = DeviceModel(name, group)
    obj.save_to_db()
    assert len(DeviceModel.find_all()) == 1

    obj.delete_from_db()
    assert len(DeviceModel.find_all()) == 0


def test_find(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = DeviceModel(name, group)
    obj.save_to_db()

    obj2 = DeviceModel.find_by_name("")
    assert obj2 is None

    obj2 = DeviceModel.find_by_name(name)
    assert obj2 is not None
