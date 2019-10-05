import unittest
from project.models.firebase import FirebaseModel
from project.db import db
from project.app import app

TEST_DB = 'test.db'

app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


class FirebaseModelTest(unittest.TestCase):
    def setUp(self):
        print("setUp")
        # self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        print("tearDown")
        db.session.remove()
        db.drop_all()

    def test_valid_user_registration(self):
        print("Test")
        imsi = "111112222233333"
        token = "AAAAAAAAAAAAAAAAAAAA"
        json_params = {'imsi': imsi, 'token': token}
        fb = FirebaseModel(imsi, token)
        json_result = fb.json()
        fb.save_to_db()
        self.assertEqual(fb.imsi, imsi)
        self.assertEqual(fb.token, token)
        self.assertEqual(json_result, json_params)


if __name__ == '__main__':
    unittest.main()
