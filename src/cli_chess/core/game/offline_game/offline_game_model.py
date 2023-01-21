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

from cli_chess.core.game import GameModelBase
from cli_chess.modules.game_options import GameOption
from cli_chess.utils.logging import log
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


class OfflineGameModel(GameModelBase):
    def __init__(self, game_parameters: dict):
        self.my_color = get_player_color(game_parameters[GameOption.COLOR])
        super().__init__(orientation=self.my_color,
                         variant=game_parameters[GameOption.VARIANT],
                         fen="")
        self._save_game_metadata(game_parameters=game_parameters)

    def _default_game_metadata(self) -> dict:
        """Returns the default structure for game metadata"""
        game_metadata = super()._default_game_metadata()
        game_metadata.update({
            'my_color': "",
            'rated': False,
            'speed': None,
        })
        return game_metadata

    def _save_game_metadata(self, **kwargs) -> None:
        """Parses and saves the data of the game being played"""
        try:
            if 'game_parameters' in kwargs:
                data = kwargs['game_parameters']
                self.game_metadata['my_color'] = self.my_color
                self.game_metadata['variant'] = data[GameOption.VARIANT]
                #self.game_metadata['players']['white'] =  # TODO: Need to set player names in offline games
                #self.game_metadata['players']['black'] =
                self.game_metadata['clock']['white']['time'] = data[GameOption.TIME_CONTROL][0]
                self.game_metadata['clock']['white']['increment'] = data[GameOption.TIME_CONTROL][1]

            self.e_game_model_updated.notify()
        except KeyError as e:
            log.error(f"Error saving offline game metadata: {e}")
