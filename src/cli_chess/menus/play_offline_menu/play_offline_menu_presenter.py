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

from __future__ import annotations
from cli_chess.menus.play_offline_menu import PlayOfflineMenuView, PlayOfflineMenuOptions
from cli_chess.menus.vs_computer_menu import VsComputerMenuModel, VsComputerMenuPresenter
from cli_chess.menus import MenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.play_offline_menu import PlayOfflineMenuModel


class PlayOfflineMenuPresenter(MenuPresenter):
    """Defines the Main Menu"""
    def __init__(self, model: PlayOfflineMenuModel):
        self.model = model
        self.vs_computer_menu_presenter = VsComputerMenuPresenter(VsComputerMenuModel())
        self.view = PlayOfflineMenuView(self)
        self.selection = self.model.get_menu_options()[0].option

        super().__init__(self.model, self.view)
