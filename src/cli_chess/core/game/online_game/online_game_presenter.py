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
from cli_chess.utils.logging import log
from chess import Color, COLOR_NAMES


def start_online_game_vs_ai(game_parameters: dict) -> None:
    """Start a game vs the lichess AI"""
    model = OnlineGameModel(game_parameters)
    presenter = OnlineGamePresenter(model)
    change_views(presenter.view, presenter.view.input_field_container) # noqa
    model.start_ai_challenge()


class OnlineGamePresenter(PlayableGamePresenterBase):
    def __init__(self, model: OnlineGameModel):
        self.model = model
        super().__init__(model)
        self.view = OnlineGameView(self)

    def update(self, **kwargs) -> None:
        """Overrides base and responds to specific model updates"""
        if 'onlineGameOver' in kwargs:
            self._parse_and_present_game_over()

    def _parse_and_present_game_over(self) -> None:
        """Handles parsing the game over status and sending it to the view for display"""
        # TODO: Break this apart into separate functions for easier readability
        if not self.is_game_in_progress():
            status = self.model.game_metadata['state']['status']
            winner = self.model.game_metadata['state']['winner'].capitalize()

            # NOTE: Status reasons must match what lichess sends via api (lila status.ts)
            status_win_reasons = ['mate', 'resign', 'timeout', 'outoftime', 'cheat', 'variantEnd']
            if winner and status in status_win_reasons:
                output = f" • {winner} is victorious"
                loser = COLOR_NAMES[not Color(COLOR_NAMES.index(winner.lower()))].capitalize()

                if status == "mate":
                    output = "Checkmate" + output
                elif status == "resign":
                    output = f"{loser} resigned" + output
                elif status == "timeout":
                    output = f"{loser} left the game" + output
                elif status == "outoftime":
                    output = f"{loser} time out" + output
                elif status == "cheat":
                    output = "Cheat detected" + output
                elif status == "variantEnd":
                    variant = self.model.game_metadata.get("variant", "")
                    if variant == "threeCheck":
                        output = "Three Checks" + output
                    elif variant == "kingOfTheHill":
                        output = "King in the center" + output
                    elif variant == "racingKings":
                        output = "Race finished" + output
                    else:
                        output = "Variant ending" + output
                else:
                    log.debug(f"OnlineGamePresenter: Received game over with uncaught status: {status} / {winner}")
                    output = "Game over" + output

            else:  # Handle other game end reasons
                if status == "aborted":
                    output = "Game aborted"
                elif status == "draw":
                    output = "Game over • Draw"
                elif status == "stalemate":
                    output = "Game over • Stalemate"
                else:
                    log.debug(f"OnlineGamePresenter: Received game over with uncaught status: {status}")
                    output = "Game over"

            # TODO: Handle not showing as "error" output if user won
            self.view.show_error(output)
