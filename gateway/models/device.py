from typing import Dict, List, Optional

from sqlalchemy import exc

from gateway import db


class DeviceModel(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    group = db.Column(db.String(15))

    def __init__(self, name: str, group: str):
        self.name: str = name
        self.group: str = group

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, group={self.group})"

    def __str__(self) -> str:
        return f"name:{self.name}, group:{self.group}"

    def json(self) -> Dict:
        return {'name': self.name, 'group': self.group}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, device_name: str) -> Optional["DeviceModel"]:
        try:
            return cls.query.filter_by(name=device_name).first()
        except exc.SQLAlchemyError:
            return None

    @classmethod
    def find_all(cls) -> Optional[List]:
        try:
            return cls.query.all()
        except exc.SQLAlchemyError:
            return None
