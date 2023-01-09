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

from cli_chess.core.game.online_game import OnlineGameModel
from cli_chess.core.game import GamePresenterBase, GameViewBase
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout


def start_online_game_vs_ai(game_parameters: dict) -> None:
    """Start a game vs the lichess ai"""
    model = OnlineGameModel(game_parameters)
    presenter = OnlineGamePresenter(model)
    model.start_ai_challenge()
    get_app().layout = Layout(presenter.game_view, presenter.game_view.input_field_container)
    get_app().invalidate()


class OnlineGamePresenter(GamePresenterBase):
    def __init__(self, model: OnlineGameModel):
        super().__init__(model)

    def make_move(self, move: str, human=True) -> None:
        try:
            self.board_presenter.make_move(move, human=human)
        except Exception as e:
            self.game_view.show_error(f"{e}")
            raise e
