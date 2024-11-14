# services/event_dispatcher.py

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def dispatch_event(self, event_name, event_data):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(event_data)
