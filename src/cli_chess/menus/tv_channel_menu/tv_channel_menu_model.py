# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from cli_chess.modules.game_options import OnlineGameOptions
from enum import Enum


class TVChannelMenuOptions(Enum):
    TOP_RATED = "Top Rated"
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
    ULTRABULLET = "UltraBullet"
    BOT = "Bot"
    COMPUTER = "Computer"

    @property
    def variant(self):
        """Return the chess variant related to the enum"""
        variant = OnlineGameOptions.variant_options_dict.get(self.value)
        if not variant:
            variant = "chess"
        return variant


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
