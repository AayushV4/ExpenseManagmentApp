from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    budget_types = db.relationship('Budget_Class')
    
class Budget_Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    budget_limit = db.Column(db.Float(15,2))
    budget_used = db.Column(db.Float(15,2))
    budget_schedule = db.Column(db.String(150))
    purchases = db.relationship('Purchases')
    
class Purchases(db.Model):
    date_time = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    name = db.Column(db.String(150))
    type_id = db.Column(db.Integer, db.ForeignKey('budget_class.id')
    money_used = db.Column(db.Float(15,2))
