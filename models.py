from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_number_masked = db.Column(db.String(20))
    expiry = db.Column(db.String(5))
    status = db.Column(db.String(20), default="PROTECTED") 

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    txn_id = db.Column(db.String(20), unique=True)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    merchant = db.Column(db.String(100))
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    location = db.Column(db.String(100))
    risk_score = db.Column(db.Float)
    status = db.Column(db.String(20))
    prediction = db.Column(db.Integer)
    reason = db.Column(db.String(255))
