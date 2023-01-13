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

from cli_chess.modules.board import BoardModel
from cli_chess.utils import Event, log
from chess import piece_symbol, WHITE, BLACK
from typing import List


class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)
        self.move_list_data = []

        self.e_move_list_model_updated = Event()
        self.update()

    def update(self, **kwargs) -> None:
        """Updates the move list data using the latest move stack"""
        self.move_list_data.clear()

        # The move replay board is used to generate the move list output
        # by replaying the move stack of the actual game on the replay board
        move_replay_board = self.board_model.board.copy()
        move_replay_board.set_fen(self.board_model.initial_fen)

        for move in self.board_model.get_move_stack():
            color = WHITE if move_replay_board.turn == WHITE else BLACK

            # Use the drop piece type if this is a crazyhouse drop
            if move.drop is None:
                piece_type = move_replay_board.piece_type_at(move.from_square)
            else:
                piece_type = move.drop

            symbol = piece_symbol(piece_type)
            is_castling = move_replay_board.is_castling(move)
            try:
                san = move_replay_board.san(move)
                move_replay_board.push_san(san)
                move_data = {
                    'turn': color,
                    'move': san,
                    'piece_type': piece_type,
                    'piece_symbol': symbol,
                    'is_castling': is_castling,
                    'is_promotion': True if move.promotion else False
                }
                self.move_list_data.append(move_data)
            except ValueError as e:
                log.error(f"Error creating move list: {e}")
                log.error(f"Move list data: {self.board_model.get_move_stack()}")
                self.move_list_data.clear()
                break

        self._notify_move_list_model_updated()

    def get_move_list_data(self) -> List[dict]:
        """Returns the move list data"""
        return self.move_list_data

    def _notify_move_list_model_updated(self) -> None:
        """Notifies listeners of move list model updates"""
        self.e_move_list_model_updated.notify()
