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
from cli_chess.core.api import IncomingEventManager, GameStream
from cli_chess.utils import Event, log
from cli_chess.modules.token_manager import TokenManagerModel
from chess import Color
from typing import Optional


class OnlineGameModel(GameModelBase):
    def __init__(self, game_parameters: dict, iem: IncomingEventManager):
        self.game_parameters = game_parameters
        self.incoming_event_manager = iem
        self.game_stream = Optional[GameStream]
        self.game_metadata = {}

        self.incoming_event_manager.e_new_event_received.add_listener(self.handle_iem_event)
        self.e_online_game_model_updated = Event()
        super().__init__()

    def handle_iem_event(self, **kwargs) -> None:
        """Handle event from the incoming event manager"""
        if 'gameStart' in kwargs:
            event = kwargs['gameStart']['game']
            if not event['hasMoved']:
                self._save_game_metadata(event)
                self._start_game_stream(event['gameId'])

        elif 'gameFinish' in kwargs:
            # TODO: End the streams, send data to presenter.
            pass

    def handle_game_stream_event(self, **kwargs) -> None:
        """Handle event from the game stream"""
        if 'gameFull' in kwargs:
            event = kwargs['gameFull']
            log.info(f"OnlineGameModel: gameFull ---- {event}")
            self.e_online_game_model_updated.notify(gameData=self.game_metadata)
            self.board_model.reinitialize_board(variant=event['variant']['key'],
                                                orientation=Color(self.game_metadata['color']),
                                                fen=event['initialFen'])
            self.board_model.make_moves_from_list(event['state']['moves'].split())

        elif 'gameState' in kwargs:
            event = kwargs['gameState']
            log.info(f"OnlineGameModel: gameState ---- {event}")

            # TODO: Key off 'status' as well to report back to presenter
            winner = event.get('winner')
            if not winner:
                moves = event['moves'].split()
                self.board_model.make_move(moves[-1])
            else:
                self.game_metadata['winner'] = winner
                self.e_online_game_model_updated.notify(gameData=self.game_metadata)

        elif 'chatLine' in kwargs:
            pass

        elif 'opponentGone' in kwargs:
            pass

    def _start_game_stream(self, game_id: str) -> None:
        """Starts streaming the events of the passed in game_id"""
        self.game_stream = GameStream(game_id)
        self.game_stream.e_new_game_stream_event.add_listener(self.handle_game_stream_event)
        self.game_stream.start()

    def _save_game_metadata(self, data: dict) -> None:
        """Parses and saves off the data of the game being played"""
        try:
            self.game_metadata['gameId'] = data['gameId']
            self.game_metadata['color'] = data['color']
            self.game_metadata['rated'] = data['rated']
            self.game_metadata['speed'] = data['speed']
            self.game_metadata['variant'] = data['variant']['name']
        except KeyError as e:
            log.error(f"Error parsing game metadata: {e}")

    def start_ai_challenge(self) -> None:
        client = TokenManagerModel().get_validated_client()
        #client.challenges.create_ai()
