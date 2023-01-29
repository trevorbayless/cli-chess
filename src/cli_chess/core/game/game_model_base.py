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

from cli_chess.modules.board import BoardModel
from cli_chess.modules.move_list import MoveListModel
from cli_chess.modules.material_difference import MaterialDifferenceModel
from cli_chess.utils.event import Event
from chess import Color, WHITE


class GameModelBase:
    def __init__(self, orientation: Color = WHITE, variant="standard", fen=""):
        self.game_metadata = self._default_game_metadata()

        self.board_model = BoardModel(orientation, variant, fen)
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)

        self.e_game_model_updated = Event()
        self.board_model.e_board_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Called automatically as part of an event listener. This function
           listens to model update events and if deemed necessary triages
           and notifies listeners of the event.
        """
        if 'board_orientation' in kwargs:
            self._notify_game_model_updated(**kwargs)

    def _notify_game_model_updated(self, **kwargs) -> None:
        """Notify listeners that the model has updated"""
        self.e_game_model_updated.notify(**kwargs)

    @staticmethod
    def _default_game_metadata() -> dict:
        """Returns the default structure for game metadata"""
        return {
            'gameId': "",
            'variant': "",
            'winner': "",
            'status': "",
            'players': {
                'white': {
                    'title': "",
                    'name': "",
                    'rating': "",
                    'provisional': False,
                },
                'black': {
                    'title': "",
                    'name': "",
                    'rating': "",
                    'provisional': False,
                },
            },
            'clock': {
                'white': {
                    'time': 0,
                    'increment': 0
                },
                'black': {
                    'time': 0,
                    'increment': 0
                },
            },
        }
