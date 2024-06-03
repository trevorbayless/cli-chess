from enum import Enum
from typing import List, Union


class MenuCategory:
    """Defines a menu with a list of associated options"""
    def __init__(self, title: str, category_options: Union[List["MenuOption"], List["MultiValueMenuOption"]]):
        self.title = title
        self.category_options = category_options


class MenuOption:
    """A menu option that has one action on enter or click (e.g. Start game)"""
    def __init__(self, option: Enum, description: str, enabled: bool = True, visible: bool = True, display_name=""):
        self.option = option
        self.option_name = display_name if display_name else self.option.value
        self.description = description
        self.enabled = enabled
        self.visible = visible


class MultiValueMenuOption(MenuOption):
    """A menu option which has multiple values to choose from (e.g. Side to play as) """
    def __init__(self, option: Enum, description: str, values: List[str], enabled: bool = True, visible: bool = True, display_name=""):
        super().__init__(option, description, enabled, visible, display_name)
        self.values = values
        self.selected_value = {
            "index": self.values.index(self.values[0]),
            "name": self.values[0]
        }

    def next_value(self):
        """Set the next value as selected"""
        if self.enabled and self.visible:
            try:
                self.selected_value["index"] = self.selected_value["index"] + 1
                self.selected_value["name"] = self.values[self.selected_value["index"]]
            except IndexError:
                self.selected_value["index"] = self.values.index(self.values[0])
                self.selected_value["name"] = self.values[self.selected_value["index"]]

    def previous_value(self):
        """Set the previous value as selected"""
        if self.enabled and self.visible:
            try:
                self.selected_value["index"] = self.selected_value["index"] - 1
                self.selected_value["name"] = self.values[self.selected_value["index"]]
            except IndexError:
                self.selected_value["index"] = self.values.index(self.values[-1])
                self.selected_value["name"] = self.values[self.selected_value["index"]]
