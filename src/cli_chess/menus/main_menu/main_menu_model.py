from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from enum import Enum


class MainMenuOptions(Enum):
    OFFLINE_GAMES = "Offline Games"
    ONLINE_GAMES = "Online Games"
    SETTINGS = "Settings"
    ABOUT = "About"


class MainMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the menu category with options"""
        menu_options = [
            MenuOption(MainMenuOptions.OFFLINE_GAMES, "Play games offline"),
            MenuOption(MainMenuOptions.ONLINE_GAMES, "Play games online using Lichess.org"),
            MenuOption(MainMenuOptions.SETTINGS, "Modify cli-chess settings"),
            MenuOption(MainMenuOptions.ABOUT, ""),
        ]

        return MenuCategory("Main Menu", menu_options)
