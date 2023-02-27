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
from chess import Color, WHITE, COLOR_NAMES
from random import getrandbits
from abc import ABC, abstractmethod


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
            'players': {
                'white': {
                    'title': "",
                    'name': "",
                    'rating': "",
                    'rating_diff': "",
                    'provisional': False,
                },
                'black': {
                    'title': "",
                    'name': "",
                    'rating': "",
                    'rating_diff': "",
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
            'state': {
                'status': "",
                'winner': "",
            }
        }


class PlayableGameModelBase(GameModelBase, ABC):
    def __init__(self, play_as_color: str, variant="standard", fen=""):
        self.my_color = self._get_side_to_play_as(play_as_color)
        self.game_in_progress = False
        super().__init__(orientation=self.my_color, variant=variant, fen=fen)

    def is_my_turn(self) -> bool:
        """Return True if it's our turn"""
        return self.board_model.get_turn() == self.my_color

    @staticmethod
    def _get_side_to_play_as(color: str) -> Color:
        """Returns a chess.Color based on the color string passed in. If the color string
           is unmatched, a random value of chess.WHITE or chess.BLACK will be returned
        """
        if color.lower() in COLOR_NAMES:
            return Color(COLOR_NAMES.index(color))
        else:  # Get random color to play as
            return Color(getrandbits(1))

    @abstractmethod
    def make_move(self, move: str) -> None:
        pass

    @abstractmethod
    def propose_takeback(self) -> None:
        pass

    @abstractmethod
    def offer_draw(self) -> None:
        pass

    @abstractmethod
    def resign(self) -> None:
        pass
