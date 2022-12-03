from app import db
from flask_login import UserMixin
from datetime import datetime


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    note = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
