# models/communication/sms_notification_strategy.py

from .notification_strategy import NotificationStrategy


class SMSNotificationStrategy(NotificationStrategy):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def notify(self, message_content: str):
        print(f"SMS sent to {self.phone_number}: {message_content}")
