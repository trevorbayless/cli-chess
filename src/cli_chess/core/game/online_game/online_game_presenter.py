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
