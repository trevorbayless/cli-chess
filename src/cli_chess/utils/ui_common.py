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
from cli_chess.utils import AlertType, log
from prompt_toolkit.layout import Window, FormattedTextControl, ConditionalContainer, D
from prompt_toolkit.filters import to_filter
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.key_binding import KeyPressEvent
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout, Container
from typing import TypeVar, Callable, cast

E = TypeVar("E", bound=Callable[[KeyPressEvent], None])
T = TypeVar("T", bound=Callable[[MouseEvent], None])


def go_back_to_main_menu() -> None:
    """Returns to the main menu"""
    from cli_chess.__main__ import main_presenter
    change_views(main_presenter.view)


def change_views(container: Container, focused_element=None):
    """Change the view to the passed in container.
       Focuses the view on the optional passed in element.
    """
    log.debug(f"Changing view to {container}")
    focused_element = focused_element if focused_element else container
    get_app().layout = Layout(container)

    try:
        get_app().layout.focus(focused_element)
    except ValueError:
        pass

    repaint_ui()


def repaint_ui() -> None:
    """Force the ui to repaint"""
    get_app().invalidate()


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


class AlertContainer:
    """A container that can be added to views to handle displaying alerts"""
    def __init__(self):
        self._alert_label = FormattedTextControl(text="", show_cursor=False)
        self._alert_container = self._create_alert_container()

    def _create_alert_container(self) -> ConditionalContainer:
        """Create the error container"""
        return ConditionalContainer(
            Window(self._alert_label, always_hide_cursor=True, height=D(max=1), wrap_lines=True),
            filter=to_filter(False)
        )

    def show_alert(self, text: str, alert_type=AlertType.ERROR) -> None:
        """Displays the alert label with the text passed in"""
        self._alert_label.text = text
        self._alert_label.style = alert_type.get_style(alert_type)
        self._alert_container.filter = to_filter(True)

    def clear_alert(self) -> None:
        """Clears the alert container"""
        self._alert_label.text = ""
        self._alert_container.filter = to_filter(False)

    def __pt_container__(self):
        return self._alert_container
