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
from cli_chess.menus import MainMenuPresenter, PlayOfflineMenuPresenter, VsComputerMenuPresenter


class RootMenuPresenter:
    def __init__(self):
        self.model = RootMenuModel()
        self.main_menu_presenter = MainMenuPresenter()
        self.play_offline_menu_presenter = PlayOfflineMenuPresenter()
        self.vs_computer_menu_presenter = VsComputerMenuPresenter()
        self.view = RootMenuView(self)
