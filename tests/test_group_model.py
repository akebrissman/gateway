from gateway.models.group import GroupModel


def test_new():
    obj = GroupModel('12345', '54321')
    assert obj.name == '12345'
    assert obj.url == '54321'
    assert obj.__repr__() == f"GroupModel(name={obj.name}, url={obj.url})"
    assert obj.__str__() == f"name:{obj.name}, url:{obj.url}"
    assert str(obj) == f"name:{obj.name}, url:{obj.url}"
    assert obj.json() == {'name': obj.name, 'url': obj.url}


def test_save_fb(app):
    name = '123456789012345'
    group = 'ABC123'
    obj1 = GroupModel(name, group)
    obj1.save_to_db()

    obj2 = GroupModel.find_by_name(name)

    assert obj1.name == obj2.name
    assert obj1.url == obj2.url

    for x in GroupModel.find_all():
        assert x.name == name


def test_save_mulitple_times(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = GroupModel(name, group)
    obj.save_to_db()
    obj.save_to_db()
    obj.save_to_db()
    assert len(GroupModel.find_all()) == 1


def test_delete(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = GroupModel(name, group)
    obj.save_to_db()
    assert len(GroupModel.find_all()) == 1

    obj.delete_from_db()
    assert len(GroupModel.find_all()) == 0


def test_find(app):
    name = '123456789012345'
    group = 'ABC123'
    obj = GroupModel(name, group)
    obj.save_to_db()

    obj2 = GroupModel.find_by_name("")
    assert obj2 is None

    obj2 = GroupModel.find_by_name(name)
    assert obj2 is not None
