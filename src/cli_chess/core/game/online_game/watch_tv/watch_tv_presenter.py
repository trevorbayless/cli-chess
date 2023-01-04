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

from cli_chess.core.game.online_game.watch_tv import WatchTVModel, WatchTVView
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.modules.board import BoardPresenter
from cli_chess.modules.material_difference import MaterialDifferencePresenter
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout


# TODO: Update the get_app() and layout calls to use MainPresenter/View to split out view logic
def start_watching_tv(channel: TVChannelMenuOptions) -> None:
    tv_presenter = WatchTVPresenter(WatchTVModel(channel))
    get_app().layout = Layout(tv_presenter.view)
    get_app().invalidate()


# TODO: Update this (as well as the view) to utilize the GamePresenterBase and GameViewBase classes
class WatchTVPresenter:
    def __init__(self, model: WatchTVModel):
        self.model = model
        self.board_presenter = BoardPresenter(self.model.board_model)
        self.material_diff_presenter = MaterialDifferencePresenter(self.model.material_diff_model)
        self.view = WatchTVView(self,
                                self.board_presenter.view,
                                self.material_diff_presenter.view_upper,
                                self.material_diff_presenter.view_lower)

        self.model.e_watch_tv_model_updated.add_listener(self.update)

        model.start_watching()

    def update(self, *args):
        """Update based on model change"""
        pass
