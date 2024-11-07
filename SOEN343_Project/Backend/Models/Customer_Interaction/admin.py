# Models/Customer_Interaction/admin.py
from dbconnection import db
from .user import User


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, name, password, email, phone_number, admin_id):
        super().__init__(name, password, email, phone_number)
        self.admin_id = admin_id  # Set admin_id without re-declaring the column
