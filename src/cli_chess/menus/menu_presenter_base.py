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

#from cli_chess.menus import MenuModelBase, MenuViewBase

class MenuPresenterBase:
    def __init__(self, model, view, menu_map):
        self.model = model
        self.view = view
        self.menu_map = menu_map

    def get_menu_options(self) -> list:
        """Returns the menu options as a list"""
        return [option.value for option in self.model.get_menu_options()]

    def show_menu(self) -> None:
        selection = self.view.show_menu()
        self.selection_handler(selection)

    def selection_handler(self, selection: str) -> None:
        """Handler for the selection made"""
        self.menu_map[self.model.get_menu_options()(selection)]()
