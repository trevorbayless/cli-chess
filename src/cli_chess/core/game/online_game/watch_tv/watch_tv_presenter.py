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

from cli_chess.core.game import GamePresenterBase
from cli_chess.core.game.online_game.watch_tv import WatchTVModel, WatchTVView
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.utils.ui_common import change_views


def start_watching_tv(channel: TVChannelMenuOptions) -> None:
    presenter = WatchTVPresenter(WatchTVModel(channel))
    change_views(presenter.view) # noqa


class WatchTVPresenter(GamePresenterBase):
    def __init__(self, model: WatchTVModel):
        self.model = model
        super().__init__(model)
        self.view = WatchTVView(self)

        self.model.e_watch_tv_model_updated.add_listener(self.update)
        self.model.start_watching()

    def update(self, *args):
        """Update based on model change"""
        pass

    def exit(self) -> None:
        """Stops TV and returns to the main menu"""
        self.model.stop_watching()
        self.view.exit()
