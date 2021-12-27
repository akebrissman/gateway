import pytest

from gateway import create_app
from gateway import db
from gateway.models.firebase import FirebaseModel


@pytest.fixture(scope='module')
def test_client():
    app = create_app('flask_test.cfg')
    app.bearer = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllrUVJ5SUdqT2ROT0RnVFB1WXp1ViJ9.eyJpc3MiOiJodHRwczovL2Ficmlzc21hbi5ldS5hdXRoMC5jb20vIiwic3ViIjoicHlkNzU1eWdGVXJ5ZlNLbThEUjlXRWlFMzl1M1RwSXZAY2xpZW50cyIsImF1ZCI6Im15LXByb2plY3QtYXBpIiwiaWF0IjoxNjQwNDU2MDE3LCJleHAiOjE2NDA1NDI0MTcsImF6cCI6InB5ZDc1NXlnRlVyeWZTS204RFI5V0VpRTM5dTNUcEl2IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.UNpa7xFg0hQc287LjHxwOlGKg-Z_ELfWA9b4Jg3XlLhWT_k2gSngWU6iA4DF3FOZvH_KKeTktqZmR4Wt5BsPURg3oRnWKa5tic6KBXgUIB_FB1xS0JH80B9iHqVPGYZfIVB0--qprzv0yDW-FOB4ccpbA9ceVzz6en4EjIof-jh7XtKnKi8AyobbNbFFUgyM-Oq17ScxZNdMQMQj3ZF95jMV1vAV8wgZhByp0lYLYeWPLNpVMBd6i-v8mqCYaZHNLl_-ZMquJkqms9czDMkLTETwO0P37W7HeE9fyq8IEDeZT9rjWjDp861s9lNarFN8uUKebdHiVfvh6eLZjZxvhA"

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_no_db():
    app = create_app('flask_test.cfg')

    with app.app_context():
        #db.create_all()
        yield app.test_client()  # this is where the testing happens!
        #db.session.remove()
        #db.drop_all()


@pytest.fixture()
def app():
    app = create_app('flask_test.cfg')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    # user1 = User(email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')
    # user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
    # db.session.add(user1)
    # db.session.add(user2)

    # Commit the changes for the users
    # db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture()
def new_fb():
    fb = FirebaseModel('123456789012345', 'guid')
    return fb
