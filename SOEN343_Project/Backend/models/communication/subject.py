# models/communication/subject.py
from .observer import Observer


class Subject:

    def attach(self, observer: Observer):
        """Attach an observer to the subject."""
        pass

    def detach(self, observer: Observer):
        """Detach an observer from the subject."""
        pass

    def notify_observers(self):
        """Notify all observers about an update."""
        pass
