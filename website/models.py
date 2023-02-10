from flask_login import UserMixin

from . import db


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

class NutritionAnalyserHistory(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    food_name = db.Column(db.String(255), nullable=False)
    imguploadpath = db.Column(db.String(255), nullable=False)
    dateprediction = db.Column(db.String(50), nullable=False)

class NutritionInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(255), nullable=False)
    serving = db.Column(db.String(50), nullable=False)
    fats = db.Column(db.String(50), nullable=False)
    protein = db.Column(db.String(50), nullable=False)
    sodium = db.Column(db.String(50), nullable=False)
    cholesterol = db.Column(db.String(50), nullable=False)
    carbohydrates = db.Column(db.String(50), nullable=False)
    sugars = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.String(50), nullable=False)
    