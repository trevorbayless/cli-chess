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
from chess import Termination, COLOR_NAMES, Color


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
        raise e


class OfflineGamePresenter(PlayableGamePresenterBase):
    def __init__(self, model: OfflineGameModel, engine_model: EngineModel):
        # NOTE: Model subscriptions are currently handled in parent. Override here if needed.
        self.model = model
        self.engine_presenter = EnginePresenter(engine_model)
        super().__init__(model)

        if self.model.board_model.get_turn() != self.model.my_color:
            asyncio.create_task(self.make_engine_move())

    def update(self, **kwargs) -> None:
        """Overrides base and responds to specific model updates"""
        if "offlineGameOver" in kwargs:
            self._parse_and_present_game_over()

    def make_move(self, move: str) -> None:
        """Make the users move on the board"""
        try:
            self.model.make_move(move)
            asyncio.create_task(self.make_engine_move())
        except Exception as e:
            self.view.show_error(f"{e}")

    async def make_engine_move(self) -> None:
        """Get the best move from the engine and make it"""
        try:
            engine_move = await self.engine_presenter.get_best_move()

            if engine_move.move:
                move = engine_move.move.uci()
                log.debug(f"OfflineGamePresenter: Sending engine move ({move}) to BoardPresenter")
                self.board_presenter.make_move(move)
        except Exception as e:
            log.critical(f"Received an invalid move from the engine: {e}")
            self.view.show_error("Invalid move received from engine - inspect logs")

    def _parse_and_present_game_over(self) -> None:
        """Handles parsing the game over status and sending it to the view for display"""
        if not self.is_game_in_progress():
            status: Termination = self.model.game_metadata['state']['status']
            winner: str = self.model.game_metadata['state']['winner'].capitalize()

            if winner and status:
                output = f" • {winner} is victorious"

                if status == Termination.CHECKMATE:
                    output = "Checkmate" + output
                elif status == Termination.VARIANT_WIN or status == Termination.VARIANT_LOSS:
                    variant = self.model.game_metadata.get("variant", "")
                    if variant == "threeCheck":
                        output = "Three Checks" + output
                    elif variant == "kingOfTheHill":
                        output = "King in the center" + output
                    elif variant == "racingKings":
                        output = "Race finished" + output
                    else:
                        output = "Variant ending" + output
                elif status == "resignation":
                    loser = COLOR_NAMES[not Color(COLOR_NAMES.index(winner.lower()))].capitalize()
                    output = f"{loser} resigned" + output
                else:
                    log.debug(f"OfflineGamePresenter: Received game over with uncaught status: {status} / {winner}")
                    output = "Game over" + output

            else:  # Handle other game end reasons
                if status == Termination.STALEMATE:
                    output = "Game over • Stalemate"
                elif (status == Termination.VARIANT_DRAW or Termination.INSUFFICIENT_MATERIAL or
                        Termination.SEVENTYFIVE_MOVES or Termination.FIVEFOLD_REPETITION or Termination.FIFTY_MOVES):
                    output = "Game over • Draw"
                else:
                    log.debug(f"OfflineGamePresenter: Received game over with uncaught status: {status}")
                    output = "Game over"

            # TODO: Handle not showing as "error" output if user won
            self.view.show_error(output)
