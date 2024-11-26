"""
This module defines the Notification class, a base class for different types
of notifications, and implements the Observer interface.
"""

from datetime import datetime  # Standard library import
from dbconnection import db  # First-party import
from .observer import Observer  # Local import


class Notification(db.Model, Observer):
    """
    Notification serves as a base class for managing notifications in the system.
    It implements the Observer interface and interacts with the database.
    """

    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message_content = db.Column(db.String, nullable=False)
    # e.g., "Pending", "Sent"
    status = db.Column(db.String(20), default="Pending")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to associate each notification with an order
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    type = db.Column(db.String(50))  # Discriminator for subclasses
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'notification'
    }

    def __init__(self, message_content, order_id):
        """
        Initialize a Notification instance with a message and associated order ID.

        Args:
            message_content (str): The notification's message content.
            order_id (int): The ID of the associated order.
        """
        self.message_content = message_content
        self.order_id = order_id

    def update(self, state: str):
        """
        Update method from Observer - overridden by subclasses.

        Args:
            state (str): The state to update the notification with.
        """
        raise NotImplementedError("Subclasses should implement this method")
