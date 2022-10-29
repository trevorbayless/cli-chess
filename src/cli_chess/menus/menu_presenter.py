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
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuCategory, MenuModel, MultiValueMenuModel, MenuView, MultiValueMenuView


class MenuPresenter:
    def __init__(self, model: MenuModel, view: MenuView):
        self.model = model
        self.view = view

    def get_menu_category(self) -> MenuCategory:
        """Get the menu category"""
        return self.model.get_menu_category()

    def get_menu_options(self) -> List[MenuOption]:
        """Returns the menu options"""
        return self.model.get_menu_options()

    def select_handler(self, selected_option: int):
        """Called on menu item selection. Classes that inherit from
           this class should override this method if they need to
           be alerted when the selected option changes
        """
        pass

    def has_focus(self):
        """Queries the view to determine if the menu has focus"""
        return self.view.has_focus()


class MultiValueMenuPresenter(MenuPresenter):
    def __init__(self, model: MultiValueMenuModel, view: MultiValueMenuView):
        self.model = model
        self.view = view
        super().__init__(self.model, self.view)

    def get_menu_options(self) -> List[MultiValueMenuOption]:
        """Returns the menu options"""
        return self.model.get_menu_options()

    def value_cycled_handler(self, selected_option: int):
        """Called when the selected options value is cycled. Classes that inherit from
           this class should override this method if they need to
           be alerted when the selected option changes
        """
        pass
