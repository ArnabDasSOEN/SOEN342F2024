"""
This module defines the Subject interface, which is part of the Observer design pattern.
Classes implementing this interface manage a list of observers and notify them of state changes.
"""

from .observer import Observer


class Subject:
    """
    Subject is an interface for objects that manage a list of observers.
    It provides methods to attach, detach, and notify observers.
    """

    def attach(self, observer: Observer):
        """
        Attach an observer to the subject.

        Args:
            observer (Observer): The observer to attach.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def detach(self, observer: Observer):
        """
        Detach an observer from the subject.

        Args:
            observer (Observer): The observer to detach.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def notify_observers(self):
        """
        Notify all observers about an update.
        """
        raise NotImplementedError("Subclasses should implement this method")
