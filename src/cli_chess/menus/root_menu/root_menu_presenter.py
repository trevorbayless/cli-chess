# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.menus.root_menu import RootMenuModel, RootMenuView
from cli_chess.menus.main_menu import MainMenuModel, MainMenuPresenter
from cli_chess.menus.play_offline_menu import PlayOfflineMenuModel, PlayOfflineMenuPresenter
from cli_chess.menus.vs_computer_menu import VsComputerMenuModel, VsComputerMenuPresenter


class RootMenuPresenter:
    def __init__(self, model: RootMenuModel):
        self.model = model
        self.main_menu_presenter = MainMenuPresenter(MainMenuModel())
        self.play_offline_menu_presenter = PlayOfflineMenuPresenter(PlayOfflineMenuModel())
        self.vs_computer_menu_presenter = VsComputerMenuPresenter(VsComputerMenuModel())
        self.view = RootMenuView(self)
