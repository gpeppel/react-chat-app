import flask_sqlalchemy
from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, pw):
        self.username = name
        self.password = pw

    def __repr__(self):
        return '<id {}>'.format(self.id)

db.create_all()

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    message = db.Column(db.String())

    def __init__(self, username, msg):
        self.username = username
        self.message = msg
    
    def __repr__(self):
        return '<Username: %s>' % self.username, '<User message: %s>' % self.message

db.create_all()