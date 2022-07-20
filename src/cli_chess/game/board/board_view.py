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
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit import HTML


class BoardView:
    def __init__(self, board_presenter: BoardPresenter, initial_board: str):
        self.board_presenter = board_presenter
        self.board_output = FormattedTextControl(HTML(initial_board))
        self.root_container = Window(self.board_output, width=20)

    def update(self, board_output: str):
        """Updates the board output with the passed in text"""
        self.board_output.text = HTML(board_output)

    def __pt_container__(self) -> Window:
        """Returns the game_view container"""
        return self.root_container
