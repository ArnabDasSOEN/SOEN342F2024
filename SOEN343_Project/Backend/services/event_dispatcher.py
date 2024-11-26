"""
Event Dispatcher
A simple implementation of an event dispatcher to manage and trigger event listeners.
"""


class EventDispatcher:
    """
    A class for managing event listeners and dispatching events to them.
    """

    def __init__(self):
        """
        Initializes the EventDispatcher with an empty dictionary for storing event listeners.
        """
        self.listeners = {}

    def add_listener(self, event_name: str, listener: callable):
        """
        Adds a listener function for a specific event.

        Args:
            event_name (str): The name of the event to listen for.
            listener (callable): A function to be called when the event is dispatched.
        """
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def dispatch_event(self, event_name: str, event_data):
        """
        Dispatches an event, triggering all listeners for the event.

        Args:
            event_name (str): The name of the event to dispatch.
            event_data: Data associated with the event, passed to each listener.
        """
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(event_data)
