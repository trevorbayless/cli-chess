from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from enum import Enum


class OnlineGamesMenuOptions(Enum):
    CREATE_GAME = "Create a game"
    VS_COMPUTER_ONLINE = "Play vs Computer"
    WATCH_LICHESS_TV = "Watch Lichess TV"


class OnlineGamesMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the menu options"""
        menu_options = [
            MenuOption(OnlineGamesMenuOptions.CREATE_GAME, "Create an online game against a random opponent"),
            MenuOption(OnlineGamesMenuOptions.VS_COMPUTER_ONLINE, "Play online against the computer"),
            MenuOption(OnlineGamesMenuOptions.WATCH_LICHESS_TV, "Watch top rated Lichess players compete live"),
        ]

        return MenuCategory("Online Games", menu_options)
