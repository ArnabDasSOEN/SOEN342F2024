# models/customer_interaction/user.py
from dbconnection import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    type = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user',
        'with_polymorphic': '*'
    }

    def __init__(self, name, password, email, phone_number):
        self.name = name
        self.password = password
        self.email = email
        self.phone_number = phone_number
