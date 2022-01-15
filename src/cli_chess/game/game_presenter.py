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

from . import GameModel, GameView
from .game_model import OfflineGameModel
from .board import BoardPresenter
from .move_list import MoveListPresenter
from .material_difference import MaterialDifferencePresenter
from .offline.engine import EnginePresenter
from chess import WHITE, BLACK
import asyncio


def play_offline() -> None:
    game_model = OfflineGameModel()
    game_presenter = OfflineGamePresenter(game_model)


class GamePresenter:
    def __init__(self, game_model: GameModel):
        self.game_model = game_model

        self.board_presenter = BoardPresenter(self.game_model.board_model)
        self.move_list_presenter = MoveListPresenter(self.game_model.move_list_model)
        self.material_diff_presenter_white = MaterialDifferencePresenter(self.game_model.material_diff_model, WHITE)
        self.material_diff_presenter_black = MaterialDifferencePresenter(self.game_model.material_diff_model, BLACK)

        self.game_view = GameView(self,
                                  self.board_presenter.view,
                                  self.move_list_presenter.view,
                                  self.material_diff_presenter_white.view,
                                  self.material_diff_presenter_black.view)

    def input_received(self, input: str) -> None:
        # TODO: Determine if this is a move, or other type of input
        self.make_move(input)

    def make_move(self, move: str) -> None:
        self.board_presenter.make_move(move)


class OfflineGamePresenter(GamePresenter):
    def __init__(self, game_model: OfflineGameModel):
        super().__init__(game_model)
        self.engine_presenter = EnginePresenter(game_model.engine_model)

    def input_received(self, input) -> None:
        super().input_received(input)
        asyncio.create_task(self.make_engine_move())

    async def make_engine_move(self) -> None:
        engine_move = await self.engine_presenter.get_best_move()
        self.make_move(engine_move.move.uci())
