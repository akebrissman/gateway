from typing import Tuple

from flask_restful import Resource, reqparse
from sqlalchemy import exc

from ..models.device import DeviceModel
from utils.decorators import requires_auth


class DeviceId(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group', type=str, required=True, location='json', help="Is mandatory!")

    @requires_auth
    def get(self, device_name: str) -> Tuple[dict, int]:
        device_model = DeviceModel.find_by_name(device_name)
        if device_model:
            return device_model.json(), 200

        return {'message': f"Device '{device_name}' not found."}, 404

    @requires_auth
    def delete(self, device_name: str) -> Tuple[dict, int]:
        device_model = DeviceModel.find_by_name(device_name)
        if device_model:
            device_model.delete_from_db()
            return {'message': 'Device deleted'}, 200

        return {'message': 'Device already deleted'}, 200

    @requires_auth
    def put(self, device_name: str) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        device_model = DeviceModel.find_by_name(device_name)

        if device_model is None:
            device_model = DeviceModel(name=device_name, group=data['group'])
        else:
            device_model.group = data['group']

        try:
            device_model.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Device."}, 500

        return device_model.json(), 200


class Device(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help="Is mandatory!")
        self.parser.add_argument('group', type=str, required=True, help="Is mandatory!")

    @requires_auth
    def get(self) -> Tuple[dict, int]:
        try:
            return {'devices': [x.json() for x in DeviceModel.find_all()]}, 200
        except Exception:
            return {"message": "An error occurred getting the Devices."}, 500

    @requires_auth
    def post(self) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        device_name = data['name']

        device_model = DeviceModel.find_by_name(device_name)

        if device_model:
            return {'message': f"Device '{device_model}' already exists."}, 400

        device_model = DeviceModel(**data)
        try:
            device_model.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Device."}, 500

        return device_model.json(), 201
