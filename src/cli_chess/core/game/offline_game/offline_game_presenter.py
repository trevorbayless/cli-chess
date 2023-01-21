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

import asyncio
from cli_chess.core.game.offline_game import OfflineGameModel
from cli_chess.core.game import PlayableGamePresenterBase
from cli_chess.modules.engine import EnginePresenter, EngineModel, create_engine_model
from cli_chess.utils.logging import log
from cli_chess.utils.ui_common import change_views


def start_offline_game(game_parameters: dict) -> None:
    """Start an offline game"""
    asyncio.create_task(_play_offline(game_parameters))


async def _play_offline(game_parameters: dict) -> None:
    try:
        model = OfflineGameModel(game_parameters)
        engine_model = await create_engine_model(model.board_model, game_parameters)

        presenter = OfflineGamePresenter(model, engine_model)
        change_views(presenter.view, presenter.view.input_field_container)
    except Exception as e:
        log.error(f"Error starting engine: {e}")
        print(e)


class OfflineGamePresenter(PlayableGamePresenterBase):
    def __init__(self, model: OfflineGameModel, engine_model: EngineModel):
        # NOTE: Model subscriptions are currently handled in parent. Override here if needed.
        super().__init__(model)
        self.engine_presenter = EnginePresenter(engine_model)

        if self.model.board_model.get_turn() != self.model.board_model.my_color:
            asyncio.create_task(self.make_engine_move())

    def make_move(self, move: str) -> None:
        """Make the users move on the board"""
        try:
            self.board_presenter.make_move(move, human=True)
            asyncio.create_task(self.make_engine_move())
        except Exception as e:
            self.view.show_error(f"{e}")

    async def make_engine_move(self) -> None:
        """Get the best move from the engine and make it"""
        try:
            self.view.lock_input()
            engine_move = await self.engine_presenter.get_best_move()
            self.board_presenter.make_move(engine_move.move.uci(), human=False)
        except Exception as e:
            log.critical(f"Received an invalid move from the engine: {e}")
            self.view.show_error(f"Invalid move received from engine - inspect logs")

        self.view.unlock_input()
