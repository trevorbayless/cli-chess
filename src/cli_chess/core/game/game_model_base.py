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

from cli_chess.modules.board import BoardModel
from cli_chess.modules.move_list import MoveListModel
from cli_chess.modules.material_difference import MaterialDifferenceModel
from random import getrandbits
import chess


def get_player_color(color: str) -> chess.Color:
    """Returns a chess.Color based on the color string passed in. If the color string
       is unmatched, a random value of chess.WHITE or chess.BLACK will be returned
    """
    if color.lower() in chess.COLOR_NAMES:
        return chess.Color(chess.COLOR_NAMES.index(color))
    else:  # Get random color to play as
        return chess.Color(getrandbits(1))


class GameModelBase:
    def __init__(self, game_parameters: dict):
        # TODO: Update to use enumeration
        self.board_model = BoardModel(my_color=get_player_color(game_parameters['Side to play as']),
                                      variant=game_parameters['Variant'])
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)
