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
from prompt_toolkit.widgets import TextArea, Box
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import D
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.modules.move_list import MoveListPresenter


class MoveListView:
    def __init__(self, presenter: MoveListPresenter):
        self.presenter = presenter
        self._move_list_output = TextArea(text="No moves...",
                                          style="class:move-list",
                                          line_numbers=True,
                                          multiline=True,
                                          wrap_lines=False,
                                          focus_on_click=False,
                                          scrollbar=False,
                                          read_only=True)
        self.key_bindings = self._create_key_bindings()
        self._container = self._create_container()

    def _create_container(self) -> Box:
        """Create the move list container"""
        return Box(self._move_list_output, height=D(max=4), padding=0)

    def update(self, formatted_move_list: List[str]):
        """Loops through the passed in move list
           and updates the move list display
        """
        # TODO: When the move list is displayed as unicode, frequently the
        #       moves do not line up. Need to rework how the container handles
        #       the text with (hopefully) not losing the ability to scroll the list
        output = ""
        for i, move in enumerate(formatted_move_list):
            if i % 2 == 0 and i != 0:
                output += "\n"
            output += move.ljust(8)

        self._move_list_output.text = output if output else "No moves..."
        self._scroll_to_bottom()

    def _scroll_to_bottom(self) -> None:
        """Scrolls the move list to the bottom"""
        line_count = self._move_list_output.buffer.document.line_count
        self._move_list_output.buffer.preferred_column = 0
        self._move_list_output.buffer.cursor_down(line_count)

    def _create_key_bindings(self) -> KeyBindings:
        """Create the key bindings for the move list"""
        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        def _(event):  # noqa
            self._move_list_output.buffer.cursor_up()

        @bindings.add(Keys.Down)
        def _(event):  # noqa
            self._move_list_output.buffer.cursor_down()

        @bindings.add(Keys.PageUp)
        def _(event):  # noqa
            self._move_list_output.buffer.preferred_column = 0
            self._move_list_output.buffer.cursor_position = 0

        @bindings.add(Keys.PageDown)
        def _(event):  # noqa
            self._scroll_to_bottom()

        return bindings

    def __pt_container__(self) -> Box:
        """Returns the move_list container"""
        return self._container
