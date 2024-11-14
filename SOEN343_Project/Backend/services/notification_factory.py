# services/notification_factory.py

from models.communication.email_notification import EmailNotification
from models.communication.sms_notification import SMSNotification
from dbconnection import db


class NotificationFactory:
    @staticmethod
    def create_notification(notification_type, message_content, contact_info, order_id):
        if notification_type == "email":
            notification = EmailNotification(
                contact_info, message_content, order_id=order_id)
        elif notification_type == "sms":
            notification = SMSNotification(
                contact_info, message_content, order_id=order_id)
        else:
            raise ValueError(f"Unknown notification type: {notification_type}")

        # Add the notification instance to the session
        db.session.add(notification)
        return notification
