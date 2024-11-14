# models/communication/notification.py

from dbconnection import db
from datetime import datetime
from .observer import Observer


class Notification(db.Model, Observer):
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
        self.message_content = message_content
        self.order_id = order_id

    def update(self, state: str):
        """Update method from Observer - overridden by subclasses."""
        raise NotImplementedError("Subclasses should implement this method")
