from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuCategory


class MenuModel:
    def __init__(self, menu_category: MenuCategory):
        self.menu_category = menu_category
        self.category_options = menu_category.category_options

    def get_menu_category(self) -> MenuCategory:
        return self.menu_category

    def get_menu_options(self) -> List[MenuOption]:
        """Returns a list containing the menu option objects"""
        if not self.menu_category.category_options:
            raise ValueError("Missing menu options")
        else:
            return self.menu_category.category_options


class MultiValueMenuModel(MenuModel):
    def __init__(self, menu_category: MenuCategory):
        super().__init__(menu_category)

    def get_menu_options(self) -> List[MultiValueMenuOption]:
        """Returns a list containing the menu option objects"""
        return super().get_menu_options()
