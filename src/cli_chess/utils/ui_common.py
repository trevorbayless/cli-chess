# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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

from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.key_binding import KeyPressEvent
from prompt_toolkit.application import get_app
from typing import TypeVar, Callable, cast

E = TypeVar("E", bound=Callable[[KeyPressEvent], None])
T = TypeVar("T", bound=Callable[[MouseEvent], None])


def exit_app(*args) -> None: # noqa
    """Exit the application"""
    get_app().exit()


def handle_bound_key_pressed(handler: E) -> E:
    """Decorator/handler for key events to avoid having to pass the key event around"""
    def bound_key_pressed(key_event: KeyPressEvent): # noqa
        return handler()

    return cast(E, bound_key_pressed)


def handle_mouse_click(handler: T) -> T:
    """Decorator to handle mouse click events"""
    def mouse_down(mouse_event: MouseEvent):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            return handler()
        else:
            return NotImplemented

    return cast(T, mouse_down)
