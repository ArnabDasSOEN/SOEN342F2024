# Models/Customer_Interaction/deliveryAgent.py
from dbconnection import db
from .user import User


class DeliveryAgent(User):
    __mapper_args__ = {
        'polymorphic_identity': 'deliveryagent',
    }

    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)
