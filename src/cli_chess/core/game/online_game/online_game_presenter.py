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

from cli_chess.core.game import PlayableGamePresenterBase
from cli_chess.core.game.online_game import OnlineGameModel, OnlineGameView
from cli_chess.utils.ui_common import change_views
from cli_chess.utils import log, AlertType
from chess import Color, COLOR_NAMES


def start_online_game(game_parameters: dict, is_vs_ai: bool) -> None:
    """Start an online game. If `is_vs_ai` is True a challenge will be sent to
       the Lichess AI (stockfish). Otherwise, a seek vs a random opponent will be created
    """
    model = OnlineGameModel(game_parameters)
    presenter = OnlineGamePresenter(model)
    change_views(presenter.view, presenter.view.input_field_container) # noqa
    model.create_a_game(is_vs_ai)


class OnlineGamePresenter(PlayableGamePresenterBase):
    def __init__(self, model: OnlineGameModel):
        self.model = model
        super().__init__(model)

    def _get_view(self) -> OnlineGameView:
        """Sets and returns the view to use"""
        return OnlineGameView(self)

    def update(self, **kwargs) -> None:
        """Update method called on game model updates. Overrides base."""
        super().update(**kwargs)
        if 'onlineGameOver' in kwargs:
            self._parse_and_present_game_over()

    def _parse_and_present_game_over(self) -> None:
        """Triages game over status for parsing and sending to the view for display"""
        if not self.is_game_in_progress():
            status: str = self.model.game_metadata['state']['status']
            winner_str = self.model.game_metadata['state']['winner']

            if winner_str:  # Handle win/loss output
                self._display_win_loss_output(status, winner_str)
            else:  # Handle draw, no start, abort output
                self._display_no_winner_output(status)
        else:
            log.error("Attempted to present game over status when the game is not over")

    def _display_win_loss_output(self, status: str, winner_str: str) -> None:
        """Generates the win/loss result reason string and sends to the view for display.
           The winner string must either be `white` or `black`.
        """
        if winner_str.lower() not in COLOR_NAMES:
            log.error(f"Received game over with invalid winner string: {winner_str} // {status}")
            self.view.alert.show_alert("Game over", AlertType.ERROR)
            return

        winner_bool = Color(COLOR_NAMES.index(winner_str))
        loser_str = COLOR_NAMES[not winner_bool].capitalize()
        output = f" • {winner_str.capitalize()} is victorious"

        # NOTE: Status strings can be found in lichess source (lila status.ts)
        if status == "mate":
            output = "Checkmate" + output
        elif status == "resign":
            output = f"{loser_str} resigned" + output
        elif status == "timeout":
            output = f"{loser_str} left the game" + output
        elif status == "outoftime":
            output = f"{loser_str} time out" + output
        elif status == "cheat":
            output = "Cheat detected" + output
        elif status == "variantEnd":
            variant = self.model.board_model.get_variant_name()
            if variant == "3check":
                output = "Three Checks" + output
            elif variant == "kingofthehill":
                output = "King in the center" + output
            elif variant == "racingkings":
                output = "Race finished" + output
            else:
                output = "Variant ending" + output
        else:
            log.debug(f"Received game over with uncaught status: {status} / {winner_str}")
            output = "Game over" + output

        alert_type = AlertType.SUCCESS if self.model.my_color == winner_bool else AlertType.ERROR
        self.view.alert.show_alert(output, alert_type)

    def _display_no_winner_output(self, status: str) -> None:
        """Generates the game result reason string and sends to the view for display.
           This function is specific to games which do not have a winner (draw, abort, etc.)
        """
        output = "Game over"
        if status:
            if status == "aborted":
                output = "Game aborted"
            if status == "noStart":
                output = "Game over • No start"
            elif status == "draw":
                output = "Game over • Draw"
            elif status == "stalemate":
                output = "Draw • Stalemate"
        else:
            log.debug(f"Received game over with uncaught status: {status}")

        self.view.alert.show_alert(output, AlertType.NEUTRAL)
