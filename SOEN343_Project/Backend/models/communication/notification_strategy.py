# models/communication/notification_strategy.py

from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message_content: str):
        raise NotImplementedError("Subclasses must implement this method")
