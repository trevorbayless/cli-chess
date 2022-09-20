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
from . import GameViewBase, GameModelBase
from .board import BoardPresenter
from .move_list import MoveListPresenter
from .material_difference import MaterialDifferencePresenter
from cli_chess.utils import log
from chess import WHITE, BLACK


class GamePresenterBase:
    def __init__(self, game_model: GameModelBase):
        self.game_model = game_model

        self.board_presenter = BoardPresenter(self.game_model.board_model)
        self.move_list_presenter = MoveListPresenter(self.game_model.move_list_model)
        self.material_diff_presenter = MaterialDifferencePresenter(self.game_model.material_diff_model)

        self.game_view = GameViewBase(self,
                                      self.board_presenter.view,
                                      self.move_list_presenter.view,
                                      self.material_diff_presenter.view_upper,
                                      self.material_diff_presenter.view_lower)

        self.game_model.board_model.e_successful_move_made.add_listener(self.game_view.clear_error)

    def user_input_received(self, input: str) -> None:
        self.make_move(input, human=True)

    def make_move(self, move: str, human=True) -> None:
        try:
            self.board_presenter.make_move(move, human=human)
        except Exception as e:
            self.game_view.show_error(f"{e}")
            raise e
