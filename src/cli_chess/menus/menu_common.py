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

from enum import Enum
from typing import List, Union


class MenuCategory:
    """Defines a menu with a list of associated options"""
    def __init__(self, title: str, category_options: Union[List["MenuOption"], List["MultiValueMenuOption"]]):
        self.title = title
        self.category_options = category_options


class MenuOption:
    """A menu option that has one action on enter or click (e.g. Start game)"""
    def __init__(self, option: Enum, description: str):
        self.option = option
        self.option_name = self.option.value
        self.description = description


class MultiValueMenuOption(MenuOption):
    """A menu option which has multiple values to choose from (e.g. Side to play as) """
    def __init__(self, option: Enum, description: str, values: List[str]):
        super().__init__(option, description)
        self.values = values
        self.selected_value = {
            "index": self.values.index(self.values[0]),
            "name": self.values[0]
        }

    def next_value(self):
        """Set the next value as selected"""
        try:
            self.selected_value["index"] = self.selected_value["index"] + 1
            self.selected_value["name"] = self.values[self.selected_value["index"]]
        except IndexError:
            self.selected_value["index"] = self.values.index(self.values[0])
            self.selected_value["name"] = self.values[self.selected_value["index"]]

    def previous_value(self):
        """Set the previous value as selected"""
        try:
            self.selected_value["index"] = self.selected_value["index"] - 1
            self.selected_value["name"] = self.values[self.selected_value["index"]]
        except IndexError:
            self.selected_value["index"] = self.values.index(self.values[-1])
            self.selected_value["name"] = self.values[self.selected_value["index"]]
