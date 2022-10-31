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

from __future__ import annotations
from prompt_toolkit.layout import ConditionalContainer, D
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.game_components.move_list import MoveListPresenter


class MoveListView:
    def __init__(self, move_list_presenter: MoveListPresenter, initial_output: str):
        self.move_list_presenter = move_list_presenter
        self.move_list_output = TextArea(text=initial_output,
                                         width=D(max=20),
                                         height=D(max=4),
                                         line_numbers=True,
                                         multiline=True,
                                         wrap_lines=False,
                                         focus_on_click=True,
                                         scrollbar=True,
                                         read_only=True)
        self.root_container = ConditionalContainer(self.move_list_output, True)

    def update(self, output: str):
        """Updates the move list output with the passed in text"""
        self.move_list_output.text = output

    def __pt_container__(self) -> ConditionalContainer:
        """Returns the move_list container"""
        return self.root_container
