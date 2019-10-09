import unittest
from db import db
from app import app

TEST_DB = 'test.db'


class FirebaseResourceTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        db.init_app(app)
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    # Helpers
    def add_firebase_via_post(self, imsi, token):
        return self.app.post(
            '/firebase',
            data=dict(token=token, imsi=imsi),
            follow_redirects=True
        )

    def update_firebase_via_put(self, imsi, token):
        return self.app.put(
            f'/firebase/{imsi}',
            data=dict(token=token),
            follow_redirects=True
        )

    def delete_firebase(self, imsi):
        return self.app.get(
            f'/logout{imsi}',
            follow_redirects=True
        )

    # Test

    def test_valid_user_registration(self):
        response = self.add_firebase_via_post(imsi='111111111111111', token='fsklisdjf')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'111111111111111', response.data)

    def test_valid_user_registration(self):
        response = self.add_firebase_via_post(imsi='111111111111111', token='fsklisdjf')
        self.assertEqual(response.status_code, 400)

    def test_main_page(self):
        response = self.app.get(f'/firebase', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        pass


if __name__ == '__main__':
    unittest.main()
