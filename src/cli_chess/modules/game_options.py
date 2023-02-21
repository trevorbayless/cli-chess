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

from cli_chess.utils.common import str_to_bool
from enum import Enum
from types import MappingProxyType
from typing import Dict


class GameOption(Enum):
    VARIANT = "Variant"
    TIME_CONTROL = "Time Control"
    COMPUTER_SKILL_LEVEL = "Computer Level"
    SPECIFY_ELO = "Specify Elo"
    COMPUTER_ELO = "Computer Elo"
    RATED = "Rated"
    RATING_RANGE = "Rating Range"
    COLOR = "Side to play as"


class BaseGameOptions:
    """Holds base options universal to Online/Offline games"""
    def __init__(self):
        self.dict_map = {}

    def create_game_parameters_dict(self, menu_selections: dict) -> Dict:
        """Lookup menu selections and replace with proper values. A dict
           is returned containing the game parameters.
        """
        game_parameters = {}
        for key in menu_selections:
            try:
                value = menu_selections[key]
                if key == GameOption.SPECIFY_ELO:
                    value = str_to_bool(value)

                opt_dict = self.dict_map.get(key)
                if opt_dict:
                    game_parameters[key] = opt_dict.get(value)
                else:
                    game_parameters[key] = value
            except KeyError:
                pass
        return game_parameters

    variant_options_dict = MappingProxyType({
        "Standard": "standard",
        "Crazyhouse": "crazyhouse",
        "Chess960": "chess960",
        "King of the Hill": "kingOfTheHill",
        "Three-check": "threeCheck",
        "Antichess": "antichess",
        "Atomic": "atomic",
        "Horde": "horde",
        "Racing Kings": "racingKings"
    })

    time_control_options_dict = MappingProxyType({
        "30+20 (Classical)": (30, 20),
        "30+0 (Classical)": (30, 0),
        "15+10 (Rapid)": (15, 10),
        "10+5 (Rapid)": (10, 5),
        "10+0 (Rapid)": (10, 0)
    })

    skill_level_options_dict = MappingProxyType({
        "Level 1": 1,
        "Level 2": 2,
        "Level 3": 3,
        "Level 4": 4,
        "Level 5": 5,
        "Level 6": 6,
        "Level 7": 7,
        "Level 8": 8
    })

    color_options = MappingProxyType({
        "Random": "random",
        "White": "white",
        "Black": "black"
    })


class OnlineGameOptions(BaseGameOptions):
    def __init__(self):
        super().__init__()
        self.dict_map = {
            GameOption.VARIANT: BaseGameOptions.variant_options_dict,
            GameOption.TIME_CONTROL: self.time_control_options_dict,
            GameOption.COMPUTER_SKILL_LEVEL: BaseGameOptions.skill_level_options_dict,
            GameOption.RATED: self.mode_options_dict,
            GameOption.RATING_RANGE: None,
            GameOption.COLOR: BaseGameOptions.color_options,
        }

    mode_options_dict = {
        "Rated": True,
        "Casual": False
    }


class OfflineGameOptions(BaseGameOptions):
    def __init__(self):
        super().__init__()
        self.dict_map = {
            GameOption.VARIANT: BaseGameOptions.variant_options_dict,
            GameOption.TIME_CONTROL: self.time_control_options_dict,
            GameOption.COMPUTER_SKILL_LEVEL: BaseGameOptions.skill_level_options_dict,
            GameOption.SPECIFY_ELO: None,
            GameOption.COMPUTER_ELO: None,
            GameOption.COLOR: BaseGameOptions.color_options,
        }

    time_control_options_dict = dict(BaseGameOptions.time_control_options_dict)
    additional_time_controls = {
        "5+3 (Blitz)": (5, 3),
        "5+0 (Blitz)": (5+0),
        "3+2 (Blitz)": (3+2),
        "3+0 (Blitz)": (3+0),
        "2+1 (Bullet)": (2+1),
        "1+0 (Bullet)": (1+0),
        "Unlimited": ("unlimited", 0)
    }
    time_control_options_dict.update(additional_time_controls)
