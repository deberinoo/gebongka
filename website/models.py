from . import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class SkinConditionHistory(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    topone = db.Column(db.String(100), nullable=False)
    toptwo = db.Column(db.String(100), nullable=False)
    topthree = db.Column(db.String(100), nullable=False)
    imguploadpath = db.Column(db.String(200), nullable=False)
    dateprediction = db.Column(db.String(80), nullable=False)
