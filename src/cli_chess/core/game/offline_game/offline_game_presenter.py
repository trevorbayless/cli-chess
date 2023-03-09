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
from cli_chess.core.game.offline_game import OfflineGameModel, OfflineGameView
from cli_chess.core.game import PlayableGamePresenterBase
from cli_chess.modules.engine import EnginePresenter, EngineModel, create_engine_model
from cli_chess.utils.ui_common import change_views
from cli_chess.utils import log, AlertType
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
        self.model = model
        self.engine_presenter = EnginePresenter(engine_model)
        super().__init__(model)

        if self.model.board_model.get_turn() != self.model.my_color:
            asyncio.create_task(self.make_engine_move())

    def _get_view(self) -> OfflineGameView:
        """Sets and returns the view to use"""
        return OfflineGameView(self)

    def update(self, **kwargs) -> None:
        """Update method called on game model updates. Overrides base."""
        if "offlineGameOver" in kwargs:
            self._parse_and_present_game_over()

    def make_move(self, move: str) -> None:
        """Make the users move on the board"""
        try:
            self.model.make_move(move)
            asyncio.create_task(self.make_engine_move())
        except Exception as e:
            self.view.show_alert(f"{e}")

    async def make_engine_move(self) -> None:
        """Get the best move from the engine and make it"""
        try:
            engine_move = await self.engine_presenter.get_best_move()

            if engine_move.resigned:
                log.debug("OfflineGamePresenter: Sending resignation on behalf of the engine")
                self.board_presenter.handle_resignation(not self.model.my_color)

            elif engine_move.move:
                move = engine_move.move.uci()
                log.debug(f"OfflineGamePresenter: Sending engine move ({move}) to BoardPresenter")
                self.board_presenter.make_move(move)
        except Exception as e:
            log.critical(f"Received an invalid move from the engine: {e}")
            self.view.show_alert("Invalid move received from engine - inspect logs")

    def _parse_and_present_game_over(self) -> None:
        """Triages game over status for parsing and sending to the view for display"""
        if not self.is_game_in_progress():
            status: Termination = self.model.game_metadata['state']['status']
            winner_str: str = self.model.game_metadata['state']['winner']

            if winner_str:  # Handle win/loss output
                self._display_win_loss_output(status, winner_str)
            else:  # Handle draw output
                self._display_draw_output(status)
        else:
            log.error("OfflineGamePresenter: In '_parse_and_present_game_over' when the game is not over")

    def _display_win_loss_output(self, status: Termination, winner_str: str) -> None:
        """Generates the win/loss result reason string and sends to the view for display.
           The winner string must either be `white` or `black`.
        """
        if winner_str.lower() not in COLOR_NAMES:
            log.error(f"OfflineGamePresenter: Received game over with invalid winner string: {winner_str} // {status}")
            self.view.show_alert("Game over", AlertType.ERROR)
            return

        winner_bool = Color(COLOR_NAMES.index(winner_str))
        output = f" • {winner_str.capitalize()} is victorious"

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
            loser = COLOR_NAMES[not winner_bool].capitalize()
            output = f"{loser} resigned" + output
        else:
            log.debug(f"OfflineGamePresenter: Received game over with uncaught status: {status} / {winner_str}")
            output = "Game over" + output

        alert_type = AlertType.SUCCESS if self.model.my_color == winner_bool else AlertType.ERROR
        self.view.show_alert(output, alert_type)

    def _display_draw_output(self, status: Termination) -> None:
        """Generates the draw result reason string and sends to the view for display"""
        output = "Draw"
        if status:
            if status == Termination.STALEMATE:
                output = output + "• Stalemate"
            elif status == Termination.VARIANT_DRAW:
                output = "Game over • Draw"
            elif status == Termination.INSUFFICIENT_MATERIAL:
                output = output + "• Insufficient material"
            elif status == Termination.THREEFOLD_REPETITION:
                output = output + "• Threefold repetition"
            elif status == Termination.FIVEFOLD_REPETITION:
                output = output + "• Fivefold repetition"
            elif status == Termination.FIFTY_MOVES:
                output = output + "• Fifty-move rule"
            elif status == Termination.SEVENTYFIVE_MOVES:
                output = output + "• Seventy-five-move rule"
        else:
            log.debug(f"OfflineGamePresenter: Received game over with uncaught status: {status}")
            output = "Game over • Draw"

        self.view.show_alert(output, AlertType.NEUTRAL)

    def exit(self) -> None:
        """Exit current presenter/view"""
        try:
            super().exit()
            asyncio.create_task(self.engine_presenter.quit_engine())
        except Exception as e:
            log.error(f"OfflineGamePresenter: Error caught while exiting: {e}")
