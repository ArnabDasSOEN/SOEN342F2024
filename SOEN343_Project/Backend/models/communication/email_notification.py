# models/communication/email_notification.py

from .notification import Notification
from dbconnection import db


class EmailNotification(Notification):
    __tablename__ = 'email_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    email = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'email_notification'
    }

    def __init__(self, email, message_content, order_id):
        super().__init__(message_content, order_id=order_id)
        self.email = email

    def update(self, state: str):
        # Update state and print the message for testing purposes
        self.message_content = f"Email sent to {
            self.email}: Your order status is now {state}"
        self.status = "Sent"
        db.session.add(self)
        db.session.commit()
        print(self.message_content)
