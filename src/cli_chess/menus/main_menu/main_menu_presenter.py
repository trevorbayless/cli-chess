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

from .main_menu_model import MainMenuModel, MainMenuOptions
from .main_menu_view import MainMenuView
from cli_chess.game import play_offline
from cli_chess.dialogs.about import show_about

menu_map = {
    MainMenuOptions.PLAY_OFFLINE: play_offline,
    MainMenuOptions.SETTINGS: None,
    MainMenuOptions.ABOUT: show_about
}


class MainMenuPresenter:
    """Defines the Main Menu"""
    def __init__(self):
        self.model = MainMenuModel()
        self.view = MainMenuView(self)

    def get_menu_options(self) -> list:
        """Return the main menu options"""
        return self.model.get_menu_options()

    def ok_handler(self) -> None:
        """Handler for the 'Ok' button"""
        menu_map[self.view.get_selected_option()]()
