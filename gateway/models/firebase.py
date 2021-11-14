from typing import Dict, List, Optional

from sqlalchemy import exc

from gateway import db


class FirebaseModel(db.Model):
    __tablename__ = 'firebase'
    id = db.Column(db.Integer, primary_key=True)
    imsi = db.Column(db.String(15))
    token = db.Column(db.String(255))

    def __init__(self, imsi: str, token: str):
        self.imsi: str = imsi
        self.token: str = token

    def __repr__(self) -> str:
        return f"{type(self).__name__}(imsi={self.imsi}, token={self.token})"

    def __str__(self) -> str:
        return f"Imsi:{self.imsi}, Token:{self.token}"

    def json(self) -> Dict:
        return {'imsi': self.imsi, 'token': self.token}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_imsi(cls, imsi: str) -> Optional["FirebaseModel"]:
        try:
            return cls.query.filter_by(imsi=imsi).first()
        except exc.SQLAlchemyError:
            return None

    @classmethod
    def find_all(cls) -> Optional[List]:
        try:
            return cls.query.all()
        except exc.SQLAlchemyError:
            return None
