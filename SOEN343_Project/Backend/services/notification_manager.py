# services/notification_manager.py

from models.communication.notification_strategy import NotificationStrategy


class NotificationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_strategy'):
            self._strategy = None

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def execute_notification(self, message_content: str):
        if self._strategy:
            self._strategy.notify(message_content)
        else:
            raise ValueError("Notification strategy is not set")
