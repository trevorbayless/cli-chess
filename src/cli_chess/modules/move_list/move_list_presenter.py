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
from cli_chess.modules.move_list import MoveListView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
from chess import BLACK, PAWN
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.modules.move_list import MoveListModel


class MoveListPresenter:
    def __init__(self, move_list_model: MoveListModel):
        self.move_list_model = move_list_model
        self.view = MoveListView(self)

        self.move_list_model.e_move_list_model_updated.add_listener(self.update)
        board_config.e_board_config_updated.add_listener(self.update)

    def update(self) -> None:
        """Update the move list output"""
        self.view.update(self.get_formatted_move_list())

    def get_formatted_move_list(self) -> List[str]:
        """Returns a list containing the formatted moves"""
        formatted_move_list = []
        move_list_data = self.move_list_model.get_move_list_data()
        use_unicode = board_config.get_boolean(board_config.Keys.USE_UNICODE_PIECES)

        for entry in move_list_data:
            move = self.get_move_as_unicode(entry) if use_unicode else (entry['move'])

            if entry['turn'] == BLACK:
                if not formatted_move_list:  # The list starts with a move from black
                    formatted_move_list.append("...")

            formatted_move_list.append(move)
        return formatted_move_list

    @staticmethod
    def get_move_as_unicode(move_data: dict) -> str:
        """Returns the passed in move data in unicode representation"""
        output = ""
        move = move_data['move']
        if move:
            output = move
            if move_data['piece_type'] != PAWN and not move_data['is_castling']:
                piece_unicode_symbol = get_piece_unicode_symbol(move_data['piece_symbol'])
                output = piece_unicode_symbol + move[1:]

            if move_data['is_promotion']:
                eq_index = output.find("=")
                if eq_index != -1:
                    promotion_unicode_symbol = get_piece_unicode_symbol(output[eq_index+1])
                    output = output[:eq_index+1] + promotion_unicode_symbol + output[eq_index+2:]

        if not output:
            output = move
        return output
