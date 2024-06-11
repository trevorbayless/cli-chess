from __future__ import annotations
from enum import Enum, auto
from typing import Callable, List


class EventTopics(Enum):
    MOVE_MADE = auto()
    BOARD_ORIENTATION_CHANGED = auto()
    GAME_PARAMS = auto()
    GAME_SEARCH = auto()
    GAME_START = auto()
    GAME_END = auto()
    ERROR = auto()


class Event:
    """Event notification class. This class creates a singular event instance
       which listeners can subscribe to with a callable. The callable will be
       notified when the event is triggered (using notify()). Generally, this
       class should not be instantiated directly, but rather from the EventManager class.
    """
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Callable) -> None:
        """Adds the passed in listener to the notification list"""
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: Callable) -> None:
        """Removes the passed in listener from the notification list"""
        if listener in self.listeners:
            self.listeners.remove(listener)

    def remove_all_listeners(self) -> None:
        """Removes all listeners associated to this event"""
        self.listeners.clear()

    def notify(self, *args, **kwargs) -> None:
        """Notifies all listeners of the event"""
        for listener in self.listeners:
            listener(*args, **kwargs)


class EventManager:
    """Event manager class. Models which use events should create
       events using this manager for easier event maintenance
    """
    def __init__(self):
        self._event_list: List[Event] = []

    def create_event(self) -> Event:
        """Creates and returns a new event for listeners to subscribe to"""
        e = Event()
        self._event_list.append(e)
        return e

    def purge_all_event_listeners(self) -> None:
        """For each event associated to this event manager
           this method will clear all listeners
        """
        for event in self._event_list:
            event.remove_all_listeners()

    def purge_all_events(self) -> None:
        """Purges all events in the event list by removing
           all associated events and listeners
        """
        self.purge_all_event_listeners()
        self._event_list.clear()
