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
from typing import TYPE_CHECKING, List, Union
if TYPE_CHECKING:
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuCategory


class MenuPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_menu_category(self) -> MenuCategory:
        return self.model.get_menu_category()

    def get_menu_options(self) -> Union[List[MenuOption], List[MultiValueMenuOption]]:
        """Returns the menu options"""
        return self.model.get_menu_options()

    def select_handler(self, selected_option: int):
        pass

    def has_focus(self):
        """Queries the view to determine if the menu has focus"""
        return self.view.has_focus()
