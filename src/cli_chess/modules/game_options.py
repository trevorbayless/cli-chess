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

from collections import ChainMap
from typing import Dict


class BaseGameOptions:
    def __init__(self, *options: dict):
        self.chain_map = ChainMap(self.color_options_dict, *options)

    def transpose_selection_dict(self, menu_selections: dict) -> Dict:
        """Lookup the key from the menu selections in the game options ChainMap
           and replace the value. Raises 'Exception' on failure.
        """
        for key in menu_selections:
            try:
                value = menu_selections[key]
                menu_selections[key] = self.chain_map[value]
            except KeyError:
                pass
        return menu_selections

    variant_options_dict = {
        "Standard": "standard",
        "Crazyhouse": "crazyhouse",
        "Chess960": "chess960",
        "King of the Hill": "kingOfTheHill",
        "Three-check": "threeCheck",
        "Antichess": "antichess",
        "Atomic": "atomic",
        "Horde": "horde",
        "Racing Kings": "racingKings",
    }

    time_control_options_dict = {
        "30+20 (Classical)": "30+20",
        "30+0 (Classical)": "30+0",
        "15+10 (Rapid)": "15+10",
        "10+5 (Rapid)": "10+5",
        "10+0 (Rapid)": "10+0"
    }

    color_options_dict = {
        "Random": "random",
        "White": "white",
        "Black": "black"
    }


class OfflineGameOptions(BaseGameOptions):
    def __init__(self):
        super().__init__(self.variant_options_dict,
                         self.time_control_options_dict,
                         self.skill_level_options_dict)

    time_control_options_dict = dict(BaseGameOptions.time_control_options_dict)
    additional_time_controls = {
        "5+3 (Blitz)": "5+3",
        "5+0 (Blitz)": "5+0",
        "3+2 (Blitz)": "3+2",
        "3+0 (Blitz)": "3+0",
        "2+1 (Bullet)": "2+1",
        "1+0 (Bullet)": "1+0",
        "Custom Time": "custom",
        "Unlimited": "unlimited"
    }
    time_control_options_dict.update(additional_time_controls)

    skill_level_options_dict = {
        # These defaults are for the Fairy Stockfish engine
        # and match what Lichess uses for their computer level settings
        "Level 1": -9,
        "Level 2": -5,
        "Level 3": -1,
        "Level 4": 3,
        "Level 5": 7,
        "Level 6": 11,
        "Level 7": 16,
        "Level 8": 20,
        "Custom Level": "custom",
        "Specify Elo": "elo"
    }


class OnlineGameOptions(BaseGameOptions):
    def __init__(self):
        super().__init__(self.variant_options_dict,
                         self.time_control_options_dict,
                         self.mode_options_dict)

    time_control_options_dict = dict(BaseGameOptions.time_control_options_dict)
    time_control_options_dict["Correspondence"] = "correspondence"

    mode_options_dict = {
        "Rated": "rated",
        "Casual": "casual"
    }

    skill_level_options_dict = {
        "Level 1": 1,
        "Level 2": 2,
        "Level 3": 3,
        "Level 4": 4,
        "Level 5": 5,
        "Level 6": 6,
        "Level 7": 7,
        "Level 8": 8
    }
