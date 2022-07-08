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

from typing import Type
from enum import Enum


class MenuModelBase:
    def __init__(self, menu_options: Type[Enum]):
        self.menu_options_type = menu_options

    def get_menu_options_type(self) -> Type[Enum]:
        """Returns the menu options enum"""
        return self.menu_options_type

    def get_menu_options(self) -> list:
        """Returns the menu options as a list"""
        return [option.value for option in self.menu_options_type]
