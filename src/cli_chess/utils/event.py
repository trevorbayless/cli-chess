# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
from typing import Callable, List


class Event:
    """Event notification class. This class creates a singular event instance
       which listeners can subscribe to with a callable. The callable will be
       notified when the event is triggered (using notify()). Generallty, this
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
