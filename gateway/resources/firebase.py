from flask_restful import Resource, reqparse
from typing import Tuple
from ..models.firebase import FirebaseModel


class FirebaseId(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, help="This field cannot be left blank!")

    def get(self, imsi: str) -> Tuple[dict, int]:
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            return fb.json(), 200

        return {'message': "Firebase item for IMSI '{}' not found.".format(imsi)}, 404

    def delete(self, imsi: str) -> Tuple[dict, int]:
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            fb.delete_from_db()
            return {'message': 'Firebase item deleted'}, 200

        return {'message': 'Firebase item already deleted'}, 200

    def put(self, imsi: str) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        fb = FirebaseModel.find_by_imsi(imsi)

        if fb is None:
            fb = FirebaseModel(imsi=imsi, token=data['token'])
        else:
            fb.token = data['token']

        try:
            fb.save_to_db()
        except:
            return {"message": "An error occurred adding the Firebase item."}, 500

        return fb.json(), 200


class Firebase(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('imsi', type=str, required=True, help="This field cannot be left blank!")
        self.parser.add_argument('token', type=str, required=True, help="This field cannot be left blank!")

    def get(self) -> Tuple[dict, int]:
        return {'items': [x.json() for x in FirebaseModel.find_all()]}, 200

    def post(self) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        imsi = data['imsi']

        fb = None
        try:
            fb = FirebaseModel.find_by_imsi(imsi)
        except:
            pass

        if fb:
            return {'message': "Firebase item for IMSI '{}' already exists.".format(imsi)}, 400

        fb = FirebaseModel(**data)
        try:
            fb.save_to_db()
        except:
            return {"message": "An error occurred adding the Firebase item."}, 500

        return fb.json(), 201
