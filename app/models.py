from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(128), index=True, unique=True)
    categories = db.Column(db.String(200), default="")
    location = db.Column(db.String(128), default="")
