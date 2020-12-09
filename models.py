import flask_sqlalchemy
from app import db


# class Usps(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(120))
    
#     def __init__(self, a):
#         self.address = a
        
#     def __repr__(self):
#         return '<Usps address: %s>' % self.address 
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, a):
        self.email = a
        
    def __repr__(self):
        return '<Account email: %s>' % self.email, '<Account password: %s>' % self.password