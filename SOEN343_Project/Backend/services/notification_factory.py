"""
Notification Factory
Provides functionality to create and manage different types of notifications.
"""

from models.communication.email_notification import EmailNotification
from models.communication.sms_notification import SMSNotification
from dbconnection import db


class NotificationFactory:
    """
    Factory class for creating notification instances.
    """

    @staticmethod
    def create_notification(notification_type: str, message_content: str, contact_info: str, order_id: int):
        """
        Creates a notification of the specified type and adds it to the database session.

        Args:
            notification_type (str): The type of notification to create ('email' or 'sms').
            message_content (str): The content of the notification message.
            contact_info (str): The recipient's contact information (e.g., email or phone number).
            order_id (int): The ID of the associated order.

        Returns:
            Notification: An instance of the created notification.

        Raises:
            ValueError: If the notification_type is not supported.
        """
        if notification_type == "email":
            notification = EmailNotification(
                contact_info=contact_info,
                message_content=message_content,
                order_id=order_id
            )
        elif notification_type == "sms":
            notification = SMSNotification(
                contact_info=contact_info,
                message_content=message_content,
                order_id=order_id
            )
        else:
            raise ValueError(f"Unknown notification type: {notification_type}")

        # Add the notification instance to the database session
        db.session.add(notification)
        return notification
