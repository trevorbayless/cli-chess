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
from typing import Callable


class Event:
    """Event notification class. Interested listeners can add a callable
       to be notified when the event is triggered (using notify()). Generally
       this is used for models to notify presenters of updated data.
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

    def notify(self, *args, **kwargs) -> None:
        """Notifies all listeners of the event"""
        for listener in self.listeners:
            listener(*args, **kwargs)
