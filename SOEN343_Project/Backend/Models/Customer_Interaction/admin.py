# models/customer_interaction/admin.py

from dbconnection import db
from .user import User


class Admin(User):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # Specific field for Admin
    admin_id = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, name, password, email, phone_number, admin_id):
        super().__init__(name, password, email, phone_number)
        self.admin_id = admin_id
