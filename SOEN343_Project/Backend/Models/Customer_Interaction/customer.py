# models/customer_interaction/customer.py

from dbconnection import db
from .user import User


class Customer(User):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Relationships with other entities
    # Link to Order with back_populates
    orders = db.relationship(
        "Order", back_populates="customer", lazy='dynamic')
    delivery_requests = db.relationship(
        "DeliveryRequest", back_populates="customer", lazy='dynamic')
    payments = db.relationship(
        "Payment", back_populates="customer", lazy='dynamic')
    # notifications = db.relationship("Notification", back_populates="customer", lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)
