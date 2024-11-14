# models/communication/sms_notification.py

from .notification import Notification
from dbconnection import db


class SMSNotification(Notification):
    __tablename__ = 'sms_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'sms_notification'
    }

    def __init__(self, phone_number, message_content, order_id):
        super().__init__(message_content, order_id=order_id)
        self.phone_number = phone_number

    def update(self, state: str):
        # Update state and print the message for testing purposes
        self.message_content = f"SMS sent to {
            self.phone_number}: Your order status is now {state}"
        self.status = "Sent"
        db.session.add(self)
        db.session.commit()
        print(self.message_content)
