# Models/Customer_Interaction/customer.py
from dbconnection import db
from .user import User


class Customer(User):
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)
