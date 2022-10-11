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
from typing import TYPE_CHECKING, Union, List
if TYPE_CHECKING:
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuCategory


class MenuModel:
    def __init__(self, menu_category: MenuCategory):
        self.menu_category = menu_category
        self.category_options = menu_category.category_options

    def get_menu_category(self) -> MenuCategory:
        return self.menu_category

    def get_menu_options(self) -> Union[List[MenuOption], List[MultiValueMenuOption]]:
        """Returns a list containing the menu option objects"""
        if not self.menu_category.category_options:
            raise ValueError("Missing menu options")
        else:
            return self.menu_category.category_options
