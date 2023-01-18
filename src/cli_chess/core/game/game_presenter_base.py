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
from cli_chess.core.game import GameViewBase, PlayableGameViewBase
from cli_chess.modules.board import BoardPresenter
from cli_chess.modules.move_list import MoveListPresenter
from cli_chess.modules.material_difference import MaterialDifferencePresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase


class GamePresenterBase:
    def __init__(self, model: GameModelBase):
        self.model = model
        self.board_presenter = BoardPresenter(model.board_model)
        self.move_list_presenter = MoveListPresenter(model.move_list_model)
        self.material_diff_presenter = MaterialDifferencePresenter(model.material_diff_model)
        self.view = GameViewBase(self)

    def flip_board(self) -> None:
        """Flip the board orientation"""
        self.model.board_model.set_board_orientation(not self.model.board_model.get_board_orientation())

    def exit(self) -> None:
        """Exit current presenter/view"""
        self.view.exit()


class PlayableGamePresenterBase(GamePresenterBase):
    def __init__(self, model: GameModelBase):
        self.model = model
        super().__init__(model)
        self.view = PlayableGameViewBase(self)

        self.model.board_model.e_successful_move_made.add_listener(self.view.clear_error)

    def user_input_received(self, inpt: str) -> None:
        self.make_move(inpt)

    def make_move(self, move: str) -> None:
        raise NotImplementedError
