from db import db


class FirebaseModel(db.Model):
    __tablename__ = 'firebase'
    id = db.Column(db.Integer, primary_key=True)
    imsi = db.Column(db.String(15))
    token = db.Column(db.String(255))

    def __init__(self, imsi, token):
        self.imsi: str = imsi
        self.token: str = token

    def __repr__(self):
        return f"<FirebaseModel {self.imsi}, {self.token}>"

    def __str__(self):
        return f"FirebaseModel {self.imsi}, {self.token}"

    def json(self):
        return {'id': self.id, 'imsi': self.imsi, 'token': self.token}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_imsi(cls, imsi):
        return cls.query.filter_by(imsi=imsi).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

