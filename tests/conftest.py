import pytest
import os
from datetime import datetime, timedelta
from jose import jwt

from gateway import create_app
from gateway import db
from gateway.models.firebase import FirebaseModel


def read_file(file_name: str) -> str:
    try:
        f = open(file_name, "r")
        data = f.read()
        f.close()
    except Exception as e:
        data = ""
    return data


def get_access_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'my-gateway-api',
              'iat': datetime.utcnow(),
              'exp': datetime.utcnow() + timedelta(seconds=10),
              'scope': 'read:group write:group'}
    headers = {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    return f"Bearer {token}"


def get_expired_access_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'my-gateway-api',
              'iat': datetime.utcnow() - timedelta(seconds=15),
              'exp': datetime.utcnow() - timedelta(seconds=5),
              'scope': 'read:group write:group'}
    headers = {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    return f"Bearer {token}"


def get_missing_kid_in_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'my-gateway-api',
              'iat': datetime.utcnow(),
              'exp': datetime.utcnow() + timedelta(seconds=10),
              'scope': 'read:group write:group'}
    headers = {}  # {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    return f"Bearer {token}"


def get_missing_scope_in_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'my-gateway-api',
              'iat': datetime.utcnow(),
              'exp': datetime.utcnow() + timedelta(seconds=30),
              'scope': 'read:device write:device'}
    headers = {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    return f"Bearer {token}"


def get_invalid_aud_in_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'INVALID',
              'iat': datetime.utcnow(),
              'exp': datetime.utcnow() + timedelta(seconds=10),
              'scope': 'read:group write:group'}
    headers = {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    return f"Bearer {token}"


def get_invalid_signature_in_token():
    claims = {'iss': 'https://abrissman.auth.com/',
              'sub': '123456789',
              'aud': 'my-gateway-api',
              'iat': datetime.utcnow(),
              'exp': datetime.utcnow() + timedelta(seconds=10),
              'scope': 'read:group write:group'}
    headers = {"kid": "123456789"}

    # TODO: Must be a better way to find the path to the file
    if os.getcwd().find('tests') >= 0:
        # Started from the IDE
        key = read_file("jwtRS256.key")
    else:
        # Started from the Terminal
        key = read_file("tests/jwtRS256.key")

    token = jwt.encode(claims=claims, key=key, algorithm='RS256', headers=headers)
    token = token + 'a'
    return f"Bearer {token}"


@pytest.fixture(scope='module')
def test_client():
    app = create_app('flask_test.cfg')
    app.bearer = get_access_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_expired_token():
    app = create_app('flask_test.cfg')
    app.bearer = get_expired_access_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_missing_kid_in_token():
    app = create_app('flask_test.cfg')
    app.bearer = get_missing_kid_in_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_missing_scope_in_token():
    app = create_app('flask_test.cfg')
    app.bearer = get_missing_scope_in_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_invalid_aud_in_token():
    app = create_app('flask_test.cfg')
    app.bearer = get_invalid_aud_in_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_invalid_signature_in_token():
    app = create_app('flask_test.cfg')
    app.bearer = get_invalid_signature_in_token()

    with app.app_context():
        db.create_all()
        yield app.test_client()  # this is where the testing happens!
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_no_db():
    app = create_app('flask_test.cfg')
    app.bearer = get_access_token()

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
