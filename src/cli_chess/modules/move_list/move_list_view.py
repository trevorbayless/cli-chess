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
from prompt_toolkit.layout import D
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.modules.move_list import MoveListPresenter


class MoveListView:
    def __init__(self, presenter: MoveListPresenter):
        self.presenter = presenter
        self.move_list_output = TextArea(text="No moves...",
                                         width=D(max=20, preferred=20),
                                         height=D(max=4, preferred=4),
                                         line_numbers=True,
                                         multiline=True,
                                         wrap_lines=False,
                                         focus_on_click=True,
                                         scrollbar=True,
                                         read_only=True)

    def update(self, formatted_move_list: List[str]):
        """Loops through the passed in move list
           and updates the move list display
        """
        output = ""
        for i, move in enumerate(formatted_move_list):
            if i % 2 == 0 and i != 0:
                output += "\n"
            output += move.ljust(8)

        if output:
            self.move_list_output.text = output
            self.move_list_output.buffer.cursor_position = len(self.move_list_output.text) - 1

    def __pt_container__(self) -> TextArea:
        """Returns the move_list container"""
        return self.move_list_output
