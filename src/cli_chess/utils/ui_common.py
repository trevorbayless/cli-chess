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
from typing import TypeVar, Callable, cast

T = TypeVar("T", bound=Callable[[MouseEvent], None])


def handle_mouse_click(handler: T) -> T:
    """Decorator to handle mouse click events"""
    def mouse_down(mouse_event: MouseEvent):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            return handler()
        else:
            return NotImplemented

    return cast(T, mouse_down)
