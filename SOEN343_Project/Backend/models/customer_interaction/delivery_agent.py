# models/customer_interaction/delivery_agent.py

from dbconnection import db
from .user import User
from models.logistics.tracker import Tracker  # Ensure Tracker is imported


class DeliveryAgent(User):
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

    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)
