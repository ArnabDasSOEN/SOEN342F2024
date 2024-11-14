# models/communication/email_notification_strategy.py

from .notification_strategy import NotificationStrategy


class EmailNotificationStrategy(NotificationStrategy):
    def __init__(self, email: str):
        self.email = email

    def notify(self, message_content: str):
        print(f"Email sent to {self.email}: {message_content}")
