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
from cli_chess.core.game.online_game import OnlineGameModel
from cli_chess.core.api import IncomingEventManager
from cli_chess.utils.ui_common import change_views


def start_online_game_vs_ai(game_parameters: dict) -> None:
    """Start a game vs the lichess ai"""
    iem = IncomingEventManager()
    iem.start()
    model = OnlineGameModel(game_parameters, iem)
    presenter = OnlineGamePresenter(model)
    model.start_ai_challenge()
    change_views(presenter.view, presenter.view.input_field_container)


class OnlineGamePresenter(PlayableGamePresenterBase):
    def __init__(self, model: OnlineGameModel):
        # NOTE: Model subscriptions are currently handled in parent. Override here if needed.
        self.model = model
        super().__init__(model)

    def make_move(self, move: str) -> None:
        """Make the move on the board"""
        try:
            if move == "0000":
                raise ValueError("Null moves are not supported in online games")
            else:
                self.board_presenter.make_move(move, human=True)
        except Exception as e:
            self.view.show_error(f"{e}")
