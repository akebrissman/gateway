from typing import Dict, List, Optional

from sqlalchemy import exc

from gateway import db


class GroupModel(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    url = db.Column(db.String(255))

    def __init__(self, name: str, url: str):
        self.name: str = name
        self.url: str = url

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, url={self.url})"

    def __str__(self) -> str:
        return f"name:{self.name}, url:{self.url}"

    def json(self) -> Dict:
        return {'name': self.name, 'url': self.url}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, group_name: str) -> Optional["GroupModel"]:
        try:
            return cls.query.filter_by(name=group_name).first()
        except exc.SQLAlchemyError:
            return None

    @classmethod
    def find_all(cls) -> Optional[List]:
        try:
            return cls.query.all()
        except exc.SQLAlchemyError:
            return None
