from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from enum import Enum


class SettingsMenuOptions(Enum):
    LICHESS_AUTHENTICATION = "Authenticate with Lichess"
    PROGRAM_SETTINGS = "Program Settings"


class SettingsMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the menu options"""
        menu_options = [
            MenuOption(SettingsMenuOptions.LICHESS_AUTHENTICATION, "Authenticate with Lichess by adding your API access token (required for playing online)"),  # noqa: E501
            MenuOption(SettingsMenuOptions.PROGRAM_SETTINGS, "Customize cli-chess"),
        ]

        return MenuCategory("General Settings", menu_options)
