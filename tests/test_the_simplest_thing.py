import flask_restful
from flask_sqlalchemy import SQLAlchemy

from gateway import db
from gateway.resources.firebase import FirebaseId


def test_true_is_not_false():

    assert True is not False


def test_db_is_a_sqlalchemy_database():

    assert isinstance(db, SQLAlchemy)


def test_firebase_id_is_a_flask_restful_resource():

    assert issubclass(FirebaseId, flask_restful.Resource)
