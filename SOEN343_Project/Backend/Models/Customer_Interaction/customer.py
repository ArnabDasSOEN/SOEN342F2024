"""
This module defines the Customer class, which extends the User class to include
customer-specific relationships and functionality.
"""

from dbconnection import db
from .user import User


class Customer(User):
    """
    The Customer class represents customers in the system, inheriting
    common attributes and functionality from the User class while adding
    relationships specific to customer activities.
    """

    __tablename__ = 'customers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Relationships with other entities
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

    # pylint: disable=useless-parent-delegation, too-few-public-methods
    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)
