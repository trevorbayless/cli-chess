from __future__ import annotations
from typing import Callable


class Event:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Callable) -> None:
        """Adds the passed in listener to the notification list"""
        self.listeners.append(listener)


    def remove_listener(self, listener: Callable) -> None:
        """Removes the passed in listener from the notification list"""
        if listener is self.listeners:
            self.listeners.remove(listener)


    def __iadd__(self, listener: Callable) -> Event:
        """Allows using += to add a listener"""
        self.add_listener(listener)
        return self

    def __isub__(self, listener: Callable) -> Event:
        """Allows using -= to remove a listener"""
        self.remove_listener(listener)
        return self


    def notify(self, *args: str, **kwargs: int) -> None:
        """Notifies all listeners of the event"""
        for listener in self.listeners:
            listener(*args, **kwargs)
