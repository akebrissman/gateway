from project.db import db
from typing import Dict, List


class FirebaseModel(db.Model):
    __tablename__ = 'firebase'
    id = db.Column(db.Integer, primary_key=True)
    imsi = db.Column(db.String(15))
    token = db.Column(db.String(255))

    def __init__(self, imsi: str, token: str):
        self.imsi: str = imsi
        self.token: str = token

    def __repr__(self) -> str:
        return f"<FirebaseModel {self.imsi}, {self.token}>"

    def __str__(self) -> str:
        return f"FirebaseModel {self.imsi}, {self.token}"

    def json(self) -> Dict:
        return {'id': self.id, 'imsi': self.imsi, 'token': self.token}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_imsi(cls, imsi: str) -> "FirebaseModel":
        return cls.query.filter_by(imsi=imsi).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

