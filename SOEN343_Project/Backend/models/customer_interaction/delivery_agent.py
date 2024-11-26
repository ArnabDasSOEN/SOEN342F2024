"""
This module defines the DeliveryAgent class, which extends the User class to include
delivery agent-specific attributes and relationships with orders and trackers.
"""

from dbconnection import db  # First-party import
from .user import User  # Local import


class DeliveryAgent(User):
    """
    The DeliveryAgent class represents delivery agents in the system. It extends
    the User class and includes relationships with orders and trackers.
    """

    __tablename__ = 'delivery_agents'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Relationships with Order and Tracker using string references
    orders = db.relationship(
        "Order", back_populates="delivery_agent", lazy='dynamic')
    trackers = db.relationship(
        "Tracker", back_populates="delivery_agent", lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'deliveryagent',
    }

    # pylint: disable=too-few-public-methods
