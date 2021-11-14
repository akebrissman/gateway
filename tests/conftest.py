import pytest

from gateway import create_app
from gateway import db
from gateway.models.firebase import FirebaseModel


@pytest.fixture(scope='module')
def test_client():
    app = create_app('flask_test.cfg')

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
