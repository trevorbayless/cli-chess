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
from cli_chess.core.api import IncomingEventManager
from cli_chess.core.api import GameStream
from cli_chess.modules.token_manager import TokenManagerModel
from chess import Color
from typing import Optional


class OnlineGameModel(GameModelBase):
    def __init__(self, game_parameters: dict):
        self.game_parameters = game_parameters
        self.incoming_event_manager = IncomingEventManager()
        self.incoming_event_manager.start()

        self.game_stream = GameStream()

        self.game_data = {}
        super().__init__()

    def _start_listening(self):
        """Start listening to game events"""
        self.incoming_event_manager.e_new_event_received.add_listener(self.handle_incoming_event)
        self.game_stream.e_new_game_stream_event.add_listener(self.handle_game_stream)

    def handle_incoming_event(self, **kwargs):
        """Handle event from the incoming event manager"""
        if 'gameStart' in kwargs:
            event = kwargs['gameStart']['game']
            if not event['hasMoved']:
                self.game_data['gameId'] = event['gameId']
                self.game_data['color'] = event['color']
                self.game_data['rated'] = event['rated']
                self.game_data['speed'] = event['speed']
                self.game_data['variant'] = event['variant']['name']

                self.game_stream.game_id = event['gameId']
                self.game_stream.start()

    def handle_game_stream(self, **kwargs):
        """Handle event from the incoming event manager"""
        if 'gameFull' in kwargs:
            event = kwargs['gameFull']
            self.board_model.reinitialize_board(variant=event['variant']['key'],
                                                orientation=Color(self.game_data['color']),
                                                fen=event['initialFen'])
            self.board_model.make_moves_from_list(event['state']['moves'].split())

        if 'gameState' in kwargs:
            event = kwargs['gameState']
            moves = event['moves'].split()
            self.board_model.make_move(moves[-1])

        if 'chatLine' in kwargs:
            pass

        if 'opponentGone' in kwargs:
            pass

    def start_ai_challenge(self):
        client = TokenManagerModel().get_validated_client()
        self._start_listening()
        #client.challenges.create_ai()
