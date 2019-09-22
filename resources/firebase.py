from flask_restful import Resource, reqparse
from models.firebase import FirebaseModel


class Firebase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('imsi', type=str, required=True, help="This field canot be left blank!")
    parser.add_argument('token', type=str, required=True, help="This field canot be left blank!")

    def get(self, imsi):
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            return fb.json(), 200

        return {'message': "Firebase item for IMSI '{}' not found.".format(imsi)}, 404

    def post(self):
        """
        Saves the imsi and token in a database.

        Returns:
        200: Success
        400: Already exist
        500: Internal error

        """
        data = Firebase.parser.parse_args()
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

    def delete(self, imsi):
        fb = FirebaseModel.find_by_imsi(imsi)
        if fb:
            fb.delete_from_db()
            return {'message': 'Firebase item deleted'}, 200

        return {'message': 'Firebase item not found'}, 404

    def put(self, imsi):
        data = Firebase.parser.parse_args()
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


class FirebaseList(Resource):
    def get(self):
        return {'items': [x.json() for x in FirebaseModel.find_all()]}
