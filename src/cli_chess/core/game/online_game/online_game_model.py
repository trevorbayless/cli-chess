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
from cli_chess.core.api import IncomingEventManager, GameStream
from cli_chess.utils import log
from cli_chess.modules.token_manager import TokenManagerModel
from chess import Color, WHITE
from typing import Optional


class OnlineGameModel(GameModelBase):
    """This model must only be used for games owned by the linked lichess user.
       Games not owned by this account must directly use the base model instead.
    """
    def __init__(self, game_parameters: dict, iem: IncomingEventManager):
        # TODO: Send None here instead on random (need to update board model logic if so)?
        self.my_color: Color = game_parameters[GameOption.COLOR] if not "random" else WHITE
        self._save_game_metadata(game_parameters=game_parameters)
        self.incoming_event_manager = iem
        self.game_stream = Optional[GameStream]

        self.incoming_event_manager.e_new_event_received.add_listener(self.handle_iem_event)
        super().__init__(orientation=self.my_color)

    def handle_iem_event(self, **kwargs) -> None:
        """Handle event from the incoming event manager"""
        # TODO: Need to ensure IEM events we are responding to in this class are specific to this game being played.
        #  Eg. We don't want to end the current game in progress, because one of our other correspondence games ended.
        if 'gameStart' in kwargs:
            event = kwargs['gameStart']['game']
            if not event['hasMoved'] and event['compat']['board']:  # TODO: There has to be a better way to ensure this is the right game...
                self._save_game_metadata(iem_gameStart=event)
                self._start_game_stream(event['gameId'])

        elif 'gameFinish' in kwargs:
            # TODO: End the streams, send data to presenter.
            pass

    def handle_game_stream_event(self, **kwargs) -> None:
        """Handle event from the game stream"""
        if 'gameFull' in kwargs:
            event = kwargs['gameFull']
            self._save_game_metadata(gs_gameFull=event)
            self.my_color = Color(self.game_metadata['my_color'])
            self.board_model.reinitialize_board(variant=self.game_metadata['variant'],
                                                orientation=self.my_color,
                                                fen=event['initialFen'])
            self.board_model.make_moves_from_list(event['state']['moves'].split())

        elif 'gameState' in kwargs:
            event = kwargs['gameState']
            log.info(f"OnlineGameModel: gameState ---- {event}")

            self.game_metadata['clock']['white']['time'] = event['wtime']
            self.game_metadata['clock']['black']['time'] = event['btime']
            self.game_metadata['status'] = event['status']
            # moves = event['moves'].split()
            # self.board_model.make_move(moves[-1])

        elif 'chatLine' in kwargs:
            pass

        elif 'opponentGone' in kwargs:
            # TODO: Start countdown if opponent is gone. Automatically claim win if timer elapses.
            pass

        self._notify_game_model_updated(gameData=self.game_metadata)

    def _start_game_stream(self, game_id: str) -> None:
        """Starts streaming the events of the passed in game_id"""
        self.game_stream = GameStream(game_id)
        self.game_stream.e_new_game_stream_event.add_listener(self.handle_game_stream_event)
        self.game_stream.start()

    def start_ai_challenge(self) -> None:
        client = TokenManagerModel().get_validated_client()
        # TODO: Use values from self.game_metadata (which should already be set) to create challenge
        #client.challenges.create_ai()

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
        """Parses and saves the data of the game being played.
           Raises an exception on invalid data.
        """
        try:
            if 'game_parameters' in kwargs:
                data = kwargs['game_parameters']
                # This is the data that came from the menu selections
                self.game_metadata['my_color'] = data[GameOption.COLOR]
                self.game_metadata['variant'] = data[GameOption.VARIANT]
                # self.game_metadata['players']['white'] =  # TODO: Need to set player names in offline games
                # self.game_metadata['players']['black'] =
                self.game_metadata['clock']['white']['time'] = data[GameOption.TIME_CONTROL][0]
                self.game_metadata['clock']['white']['increment'] = data[GameOption.TIME_CONTROL][1]
                self.game_metadata['clock']['black'] = self.game_metadata['clock']['white']

            if 'iem_gameStart' in kwargs:
                data = kwargs['iem_gameStart']
                log.debug(f"OnlineGameModel: iem_gameStart ---- {data}")  # TODO: Remove after testing
                self.game_metadata['gameId'] = data['gameId']
                self.game_metadata['my_color'] = data['color']  # TODO: Update to use bool instead? Color(data['color')
                self.game_metadata['rated'] = data['rated']
                self.game_metadata['variant'] = data['variant']['name']
                self.game_metadata['speed'] = data['speed']
                log.debug(f"self.game_metadata ---- {self.game_metadata}")  # TODO: Remove after testing

            elif 'gs_gameFull' in kwargs:
                data = kwargs['gs_gameFull']
                log.debug(f"OnlineGameModel: gs_gameFull ---- {data}")  # TODO: Remove after testing
                self.game_metadata['players']['white'] = data['white']
                self.game_metadata['players']['black'] = data['black']
                self.game_metadata['clock']['white']['time'] = data['state']['wtime']
                self.game_metadata['clock']['white']['increment'] = data['state']['winc']
                self.game_metadata['clock']['black']['time'] = data['state']['btime']
                self.game_metadata['clock']['black']['increment'] = data['state']['binc']
                log.debug(f"self.game_metadata ---- {self.game_metadata}")  # TODO: Remove after testing

            self._notify_game_model_updated()
        except Exception as e:
            log.exception(f"Error saving online game metadata: {e}")
            raise
