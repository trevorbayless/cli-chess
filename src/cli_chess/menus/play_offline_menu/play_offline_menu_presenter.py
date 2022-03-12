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

from cli_chess.menus import MenuPresenterBase, PlayOfflineMenuOptions
from .play_offline_menu_model import PlayOfflineMenuModel
from .play_offline_menu_view import PlayOfflineMenuView
from .vs_computer import show_vs_computer_menu

menu_map = {
    PlayOfflineMenuOptions.VS_COMPUTER: show_vs_computer_menu,
    PlayOfflineMenuOptions.BOTH_SIDES: None,
    PlayOfflineMenuOptions.PUZZLES: None,
}


def show_play_offline_menu():
    """Show the Play Offline menu"""
    PlayOfflineMenuPresenter().show_menu()


class PlayOfflineMenuPresenter(MenuPresenterBase):
    """Define the menu"""
    def __init__(self):
        super().__init__(PlayOfflineMenuModel(), PlayOfflineMenuView(self), menu_map)
