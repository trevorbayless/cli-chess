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

from cli_chess.utils.logging import log
from collections import ChainMap
from typing import Dict


class BaseGameOptions:
    def __init__(self, *options: dict):
        self.chain_map = ChainMap(self.color_options_dict, *options)

    def transpose_selection_dict(self, menu_selections: dict) -> Dict:
        """Lookup the key from the menu selections in the
           game options ChainMap and replace the value
        """
        for key in menu_selections:
            try:
                value = menu_selections[key]
                menu_selections[key] = self.chain_map[value]
            except KeyError:
                log.exception(f"Error transposing dict: key={key} value={menu_selections[key]}")
                raise

        return menu_selections

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

    variant_options_dict = {
        "Standard": "chess",
        "Crazyhouse": "crazyhouse",
        "Chess960": "chess960",
        "King of the Hill": "kingofthehill",
        "Three-check": "3check",
        "Antichess": "antichess",
        "Atomic": "atomic",
        "Horde": "horde",
        "Racing Kings": "racingkings",
        "From Position": "setup"
    }

    time_control_options_dict = {
        "Custom Time": "custom",
        "Unlimited": "unlimited",
        "30+20 (Classical)": "30+20",
        "30+0 (Classical)": "30+0",
        "15+10 (Rapid)": "15+10",
        "10+5 (Rapid)": "10+5",
        "10+0 (Rapid)": "10+0",
        "5+3 (Blitz)": "5+3",
        "5+0 (Blitz)": "5+0",
        "3+2 (Blitz)": "3+2",
        "3+0 (Blitz)": "3+0",
        "2+1 (Bullet)": "2+1",
        "1+0 (Bullet)": "1+0"
    }

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
        "Custom Level": "custom"
    }


class OnlineGameOptions(BaseGameOptions):
    def __init__(self):
        super().__init__(self.variant_options_dict,
                         self.time_control_options_dict,
                         self.mode_options_dict)

    variant_options_dict = {
        "Standard": "standard",
        "Crazyhouse": "zh",
        "Chess960": "chess960",
        "King of the Hill": "koth",
        "Three-check": "3check",
        "Antichess": "anti",
        "Atomic": "atomic",
        "Horde": "horde",
        "Racing Kings": "race",
    }

    time_control_options_dict = {
        "30+20 (Classical)": "30+20",
        "30+0 (Classical)": "30+0",
        "15+10 (Rapid)": "15+10",
        "10+5 (Rapid)": "10+5",
        "10+0 (Rapid)": "10+0",
        "Correspondence": "correspondence",
        "Custom": "custom",
    }

    mode_options_dict = {
        "Casual": "casual",
        "Rated": "rated"
    }
