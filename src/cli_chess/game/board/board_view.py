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
    def __init__(self, board_presenter: BoardPresenter, initial_board_output: list):
        self.board_presenter = board_presenter
        self.board_output = FormattedTextControl(HTML(self._build_output(initial_board_output)))
        self.root_container = Window(self.board_output, width=20)

    def _build_output(self, board_output_list: list) -> str:
        """Returns a string containing the board output to be used for
           display. The string returned will contain HTML elements"""
        board_output_str = ""
        file_label_color = self.board_presenter.get_file_labels_color()
        rank_label_color = self.board_presenter.get_rank_labels_color()

        for square in board_output_list:
            # Pad piece for proper alignment
            piece_str = square['piece_str']
            piece_str += " " if square['piece_str'] else "  "

            board_output_str += f"<style fg='{rank_label_color}'>{square['rank_label']}</style>"
            board_output_str += f"<style fg='{square['piece_display_color']}' bg='{square['square_display_color']}'>{piece_str}</style>"

            if square['is_end_of_rank']:
                board_output_str += "\n"

        file_labels = " " + self.board_presenter.get_file_labels()
        board_output_str += f"<style fg='{file_label_color}'>{file_labels}</style>"

        return board_output_str

    def update(self, board_output_list: list):
        """Updates the board output with the passed in text"""
        self.board_output.text = HTML(self._build_output(board_output_list))

    def __pt_container__(self) -> Window:
        """Returns the game_view container"""
        return self.root_container
