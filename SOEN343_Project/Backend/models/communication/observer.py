"""
This module defines the Observer interface, which is part of the Observer design pattern.
Classes implementing this interface should define the `update` method.
"""


class Observer:
    """
    Observer is an interface for objects that need to be notified of state changes
    in subjects they observe. Subclasses must implement the `update` method.
    """

    def update(self, state: str):
        """
        Update the observer based on the subject's state change.

        Args:
            state (str): The new state of the subject.
        """
        raise NotImplementedError("Subclasses should implement this method")
