from cli_chess.utils.common import str_to_bool
from enum import Enum
from types import MappingProxyType
from typing import Dict
from abc import ABC, abstractmethod


class GameOption(Enum):
    VARIANT = "Variant"
    TIME_CONTROL = "Time Control"
    COMPUTER_SKILL_LEVEL = "Computer Level"
    SPECIFY_ELO = "Specify Elo"
    COMPUTER_ELO = "Computer Elo"
    RATED = "Rated"
    RATING_RANGE = "Rating Range"
    COLOR = "Side to play as"


class BaseGameOptions(ABC):
    """Holds base options universal to Online/Offline games"""
    @abstractmethod
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


class OfflineGameOptions(BaseGameOptions):
    """Game Options class with defined options for playing offline games"""
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
        "5+0 (Blitz)": (5, 0),
        "3+2 (Blitz)": (3, 2),
        "3+0 (Blitz)": (3, 0),
        "2+1 (Bullet)": (2, 1),
        "1+0 (Bullet)": (1, 0),
    }
    time_control_options_dict.update(additional_time_controls)


class OnlineGameOptions(BaseGameOptions):
    """Game Options class with defined options permitted for board API use"""
    def __init__(self):
        super().__init__()
        self.dict_map = {
            GameOption.VARIANT: BaseGameOptions.variant_options_dict,
            GameOption.TIME_CONTROL: self.time_control_options_dict,
            GameOption.COMPUTER_SKILL_LEVEL: BaseGameOptions.skill_level_options_dict,
            GameOption.RATED: self.rated_options_dict,
            GameOption.RATING_RANGE: None,
            GameOption.COLOR: BaseGameOptions.color_options,
        }

    rated_options_dict = {
        "No": False,
        "Yes": True
    }


class OnlineDirectChallengesGameOptions(OnlineGameOptions):
    """Game Options class with defined options for direct challenges.
       Brings in the additional permitted time controls.
    """
    def __init__(self):
        super().__init__()

    time_control_options_dict = dict(BaseGameOptions.time_control_options_dict)
    additional_time_controls = {
        "5+3 (Blitz)": (5, 3),
        "5+0 (Blitz)": (5, 0),
        "3+2 (Blitz)": (3, 2),
        "3+0 (Blitz)": (3, 0)
    }
    time_control_options_dict.update(additional_time_controls)
