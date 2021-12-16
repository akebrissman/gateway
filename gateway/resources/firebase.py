from typing import Tuple

from flask_restful import Resource, reqparse
from sqlalchemy import exc

from ..models.firebase import FirebaseModel


class FirebaseId(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, help="Is mandatory!")

    def get(self, imsi: str) -> Tuple[dict, int]:
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            return fb.json(), 200

        return {'message': "Firebase item for IMSI '{}' not found.".format(imsi)}, 404

    def delete(self, imsi: str) -> Tuple[dict, int]:
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            fb.delete_from_db()
            return {'message': 'Firebase deleted'}, 200

        return {'message': 'Firebase already deleted'}, 200

    def put(self, imsi: str) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        fb = FirebaseModel.find_by_imsi(imsi)

        if fb is None:
            fb = FirebaseModel(imsi=imsi, token=data['token'])
        else:
            fb.token = data['token']

        try:
            fb.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Firebase."}, 500

        return fb.json(), 200


class Firebase(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('imsi', type=str, required=True, help="Is mandatory!")
        self.parser.add_argument('token', type=str, required=True, help="Is mandatory!")

    def get(self) -> Tuple[dict, int]:
        try:
            return {'items': [x.json() for x in FirebaseModel.find_all()]}, 200
        except exc.SQLAlchemyError:
            return {"message": "An error occurred getting the Firebase."}, 500

    def post(self) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        imsi = data['imsi']

        fb = FirebaseModel.find_by_imsi(imsi)

        if fb:
            return {'message': f"Firebase item for IMSI '{imsi}' already exists."}, 400

        fb = FirebaseModel(**data)
        try:
            fb.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Firebase."}, 500

        return fb.json(), 201
