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

from cli_chess.menus import MenuPresenterBase, MainMenuOptions
from .main_menu_model import MainMenuModel
from .main_menu_view import MainMenuView

from cli_chess.menus.play_offline_menu import show_play_offline_menu

menu_map = {
    MainMenuOptions.PLAY_OFFLINE: show_play_offline_menu,
    MainMenuOptions.QUIT: quit
}


class MainMenuPresenter(MenuPresenterBase):
    """Defines the Main Menu"""
    def __init__(self):
        super().__init__(MainMenuModel(), MainMenuView(self), menu_map)
