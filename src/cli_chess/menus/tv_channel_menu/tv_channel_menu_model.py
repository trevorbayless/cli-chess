from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from cli_chess.core.game.game_options import OnlineGameOptions
from types import MappingProxyType
from enum import Enum

tv_key_dict = MappingProxyType({
    "Top Rated": "best",
    "Ultra Bullet": "ultraBullet",
    "Bullet": "bullet",
    "Blitz": "blitz",
    "Rapid": "rapid",
    "Classical": "classical",
    "Crazyhouse": "crazyhouse",
    "Chess960": "chess960",
    "King of the Hill": "kingOfTheHill",
    "Three-check": "threeCheck",
    "Antichess": "antichess",
    "Atomic": "atomic",
    "Horde": "horde",
    "Racing Kings": "racingKings",
    "Bot": "bot",
    "Computer": "computer"
})


class TVChannelMenuOptions(Enum):
    TOP_RATED = "Top Rated"
    ULTRABULLET = "Ultra Bullet"
    BULLET = "Bullet"
    BLITZ = "Blitz"
    RAPID = "Rapid"
    CLASSICAL = "Classical"
    CRAZYHOUSE = "Crazyhouse"
    CHESS960 = "Chess960"
    KING_OF_THE_HILL = "King of the Hill"
    THREE_CHECK = "Three-check"
    ANTICHESS = "Antichess"
    ATOMIC = "Atomic"
    HORDE = "Horde"
    RACING_KINGS = "Racing Kings"
    BOT = "Bot"
    COMPUTER = "Computer"

    @property
    def variant(self) -> str:
        """Return the chess variant related to the enum"""
        variant = OnlineGameOptions.variant_options_dict.get(self.value)
        if not variant:
            variant = "standard"
        return variant

    @property
    def key(self) -> str:
        """Returns the channel key used in api transactions"""
        return tv_key_dict.get(self.value)


class TVChannelMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the menu options"""
        menu_options = []
        for channel in TVChannelMenuOptions:
            menu_options.append(MenuOption(channel, ""))
        return MenuCategory("TV Channels", menu_options)
