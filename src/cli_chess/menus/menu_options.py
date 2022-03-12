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


class MainMenuOptions(Enum):
    PLAY_OFFLINE = "Play Offline"
    SETTINGS = "Settings"
    ABOUT = "About"
    QUIT = "Quit"


class PlayOfflineMenuOptions(Enum):
    VS_COMPUTER = "Play vs Computer"
    BOTH_SIDES = "Play both sides"
    PUZZLES = "Solve Puzzles"


class GameOptions:
    class VariantOptions(Enum):
        STANDARD = "Standard"
        CRAZYHOUSE = "Crazyhouse"
        CHESS960 = "Chess960"
        KING_OF_THE_HILL = "King of the Hill"
        THREE_CHECK = "Three-check"
        ANTICHESS = "Antichess"
        ATOMIC = "Atomic"
        HORDE = "Horde"
        RACING_KINGS = "Racing Kings"
        FROM_POSITION = "From Position"

    class TimeControlOptions(Enum):
        REAL_TIME = "Real Time"
        UNLIMITED = "Unlimited"

    class ModeOptions(Enum):
        CASUAL = "Casual"
        RATED = "Rated"

    class ColorOptions(Enum):
        RANDOM = "Random"
        WHITE = "White"
        BLACK = "Black"

    class StrengthOptions(Enum):
        ELO_BASED = "Set Computers ELO"
        LEVEL_BASED = "Choose Computers Level"