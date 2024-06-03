from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from enum import Enum


class OfflineGamesMenuOptions(Enum):
    VS_COMPUTER = "Play vs Computer"


class OfflineGamesMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the menu options"""
        menu_options = [
            MenuOption(OfflineGamesMenuOptions.VS_COMPUTER, "Play offline against the computer")
        ]

        return MenuCategory("Offline Games", menu_options)
