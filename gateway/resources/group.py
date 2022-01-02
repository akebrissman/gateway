from typing import Tuple

from flask_restful import Resource, reqparse
from sqlalchemy import exc

from ..models.group import GroupModel
from ..utils.decorators import requires_auth_with_scope


class GroupId(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('url', type=str, required=True, location='json', help="Is mandatory!")

    @requires_auth_with_scope('read:group')
    def get(self, group_name: str) -> Tuple[dict, int]:
        group_model = GroupModel.find_by_name(group_name)
        if group_model:
            return group_model.json(), 200

        return {'message': f"Group '{group_name}' not found."}, 404

    @requires_auth_with_scope('write:group')
    def delete(self, group_name: str) -> Tuple[dict, int]:
        group_model = GroupModel.find_by_name(group_name)
        if group_model:
            group_model.delete_from_db()
            return {'message': 'Group deleted'}, 200

        return {'message': 'Group already deleted'}, 200

    @requires_auth_with_scope('write:group')
    def put(self, group_name: str) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        group_model = GroupModel.find_by_name(group_name)

        if group_model is None:
            group_model = GroupModel(name=group_name, url=data['url'])
        else:
            group_model.url = data['url']

        try:
            group_model.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Group."}, 500

        return group_model.json(), 200


class Group(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help="Is mandatory!")
        self.parser.add_argument('url', type=str, required=True, help="Is mandatory!")

    @requires_auth_with_scope('read:group')
    def get(self) -> Tuple[dict, int]:
        try:
            return {'groups': [x.json() for x in GroupModel.find_all()]}, 200
        except Exception:
            return {"message": "An error occurred getting the Groups."}, 500

    @requires_auth_with_scope('write:group')
    def post(self) -> Tuple[dict, int]:
        data = self.parser.parse_args()
        group_name = data['name']

        group_model = GroupModel.find_by_name(group_name)

        if group_model:
            return {'message': f"Group '{group_model}' already exists."}, 409

        group_model = GroupModel(**data)
        try:
            group_model.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred adding the Group."}, 500

        return group_model.json(), 201
