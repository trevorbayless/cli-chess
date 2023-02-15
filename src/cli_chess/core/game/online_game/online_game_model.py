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
from cli_chess.core.api import GameStateDispatcher
from cli_chess.utils import log, threaded
from chess import Color, COLOR_NAMES, WHITE
from typing import Optional


class OnlineGameModel(GameModelBase):
    """This model must only be used for games owned by the linked lichess user.
       Games not owned by this account must directly use the base model instead.
    """
    def __init__(self, game_parameters: dict):
        # TODO: Send None here instead on random (need to update board model logic if so)?
        self.my_color: Color = game_parameters[GameOption.COLOR] if not "random" else WHITE
        super().__init__(variant=game_parameters[GameOption.VARIANT], orientation=self.my_color, fen=None)
        self._save_game_metadata(game_parameters=game_parameters)

        self.game_state_dispatcher = Optional[GameStateDispatcher]
        self.game_in_progress = False
        self.playing_game_id = None

        try:
            from cli_chess.core.api.api_manager import api_client, api_iem
            self.api_iem = api_iem
            self.api_client = api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("OnlineGameModel: Failed to import api_iem and api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

    @threaded
    def start_ai_challenge(self) -> None:
        """Sends a request to lichess to start an AI challenge using the selected game parameters"""
        # Note: Only add IEM listener right before creating event to lessen chance of grabbing another game
        self._subscribe_to_iem_events()
        self.api_client.challenges.create_ai(level=self.game_metadata['ai_level'],
                                             clock_limit=self.game_metadata['clock']['white']['time'],
                                             clock_increment=self.game_metadata['clock']['white']['increment'],
                                             color=self.game_metadata['my_color'],
                                             variant=self.game_metadata['variant'])

    def _start_game(self, game_id: str) -> None:
        """Called when a game is started. Sets proper class variables
           and starts and registers game stream event callback
        """
        if game_id and not self.game_in_progress:
            self.game_in_progress = True
            self.playing_game_id = game_id

            self.game_state_dispatcher = GameStateDispatcher(game_id)
            self.game_state_dispatcher.e_game_state_dispatcher_event.add_listener(self.handle_game_state_dispatcher_event)
            self.game_state_dispatcher.start()

    def _game_end(self) -> None:
        """The game we are playing has ended. Handle cleaning up."""
        self.game_in_progress = False
        self.playing_game_id = None
        self._unsubscribe_from_iem_events()
        self.game_state_dispatcher.clear_listeners()

    def handle_iem_event(self, **kwargs) -> None:
        """Handle event from the incoming event manager"""
        # TODO: Need to ensure IEM events we are responding to in this class are specific to this game being played.
        #  Eg. We don't want to end the current game in progress, because one of our other correspondence games ended.
        if 'gameStart' in kwargs:
            event = kwargs['gameStart']['game']
            log.info("IEM: got a game start event")
            # TODO: There has to be a better way to ensure this is the right game...
            #  add some further specific clauses like color, time control, date, etc?
            if not self.game_in_progress and not event['hasMoved'] and event['compat']['board']:
                log.info("IEM: PICKED UP AND STARTED GAME")
                self._save_game_metadata(iem_gameStart=event)
                self._start_game(event['gameId'])

        elif 'gameFinish' in kwargs:
            event = kwargs['gameFinish']['game']
            if self.game_in_progress and self.playing_game_id == event['gameId']:
                self._save_game_metadata(iem_gameFinish=event)
                self._game_end()

    def handle_game_state_dispatcher_event(self, **kwargs) -> None:
        """Handle event from the game stream"""
        if 'gameFull' in kwargs:
            event = kwargs['gameFull']
            self._save_game_metadata(gsd_gameFull=event)
            self.my_color = Color(COLOR_NAMES.index(self.game_metadata['my_color']))
            self.board_model.reinitialize_board(variant=self.game_metadata['variant'],
                                                orientation=self.my_color,
                                                fen=event['initialFen'])
            self.board_model.make_moves_from_list(event['state']['moves'].split())

        elif 'gameState' in kwargs:
            event = kwargs['gameState']
            self._save_game_metadata(gsd_gameState=event)

            # TODO: Take some time measurements to see how much of an impact this approach is
            # Resetting and replaying the moves guarantees the game between lichess
            # and our local board are in sync (eg. takebacks, moves played on website, etc)
            self.board_model.reset(notify=False)
            self.board_model.make_moves_from_list(event['moves'].split())

        elif 'chatLine' in kwargs:
            event = kwargs['chatLine']
            self._save_game_metadata(gsd_chatLine=event)

        elif 'opponentGone' in kwargs:
            # TODO: Show alert to user
            event = kwargs['opponentGone']
            self._save_game_metadata(gsd_opponentGone=event)

    def make_move(self, move: str):
        """Sends the move to the board model for a validity check. If valid this
           function will pass the move over to the game state dispatcher to be sent
           Raises an exception on move or API errors.
        """
        if self.game_in_progress and move:
            try:
                if move == "0000":
                    raise ValueError("Null moves are not supported in online games")

                move = self.board_model.verify_move(move)

                log.info(f"OnlineGameModel: Sending move ({move}) to lichess")
                self.game_state_dispatcher.make_move(move)
            except Exception:
                raise
        else:
            log.error("OnlineGameModel: Attempted to make a move in a game that's not in progress")
            raise Exception("Game is not in progress")

    def propose_takeback(self) -> None:
        """Notifies the game state dispatcher to propose a takeback"""
        if self.game_in_progress:
            try:
                # TODO: Handle repeat spams
                self.game_state_dispatcher.send_takeback_request()
            except Exception:
                raise
        else:
            log.error("OnlineGameModel: Attempted to propose a takeback in a game that's not in progress")
            raise Exception("Game is not in progress")

    def offer_draw(self) -> None:
        """Notifies the game state dispatcher to offer a draw"""
        if self.game_in_progress:
            try:
                # TODO: Handle repeat spams
                self.game_state_dispatcher.send_draw_offer()
            except Exception:
                raise
        else:
            log.error("OnlineGameModel: Attempted to offer a draw to a game that's not in progress")
            raise Exception("Game is not in progress")

    def resign(self) -> None:
        """Notifies the game state dispatcher to resign the game"""
        if self.game_in_progress:
            try:
                self.game_state_dispatcher.resign()
            except Exception:
                raise
        else:
            log.error("OnlineGameModel: Attempted to resign a game that's not in progress")
            raise Exception("Game is not in progress")

    def _save_game_metadata(self, **kwargs) -> None:
        """Parses and saves the data of the game being played.
           If notify is false, a model update notification will not be sent.
           Raises an exception on invalid data.
        """
        try:
            if 'game_parameters' in kwargs:  # This is the data that came from the menu selections
                data = kwargs['game_parameters']
                self.game_metadata['my_color'] = data[GameOption.COLOR]
                self.game_metadata['variant'] = data[GameOption.VARIANT]
                self.game_metadata['rated'] = data.get(GameOption.RATED, False)  # Games against ai will not have this data
                self.game_metadata['ai_level'] = data.get(GameOption.COMPUTER_SKILL_LEVEL)  # Only games against ai will have this data
                self.game_metadata['clock']['white']['time'] = data[GameOption.TIME_CONTROL][0] * 60  # secs
                self.game_metadata['clock']['white']['increment'] = data[GameOption.TIME_CONTROL][1]  # secs
                self.game_metadata['clock']['black'] = self.game_metadata['clock']['white']

            elif 'iem_gameStart' in kwargs:
                data = kwargs['iem_gameStart']
                self.game_metadata['gameId'] = data['gameId']
                self.game_metadata['my_color'] = data['color']  # TODO: Update to use bool instead? Color(data['color')
                self.game_metadata['rated'] = data['rated']
                self.game_metadata['variant'] = data['variant']['name']
                self.game_metadata['speed'] = data['speed']

            elif 'gsd_gameFull' in kwargs:
                data = kwargs['gsd_gameFull']

                for color in COLOR_NAMES:
                    if data[color].get('name'):
                        self.game_metadata['players'][color]['title'] = data[color]['title']
                        self.game_metadata['players'][color]['name'] = data[color]['name']
                        self.game_metadata['players'][color]['rating'] = data[color]['rating']
                        self.game_metadata['players'][color]['provisional'] = data[color]['provisional']
                    elif data[color].get('aiLevel'):
                        self.game_metadata['players'][color]['title'] = ""
                        self.game_metadata['players'][color]['name'] = f"Stockfish level {data[color]['aiLevel']}"
                        self.game_metadata['players'][color]['rating'] = ""
                        self.game_metadata['players'][color]['provisional'] = False

                # NOTE: Times below come from lichess in milliseconds
                self.game_metadata['clock']['white']['time'] = data['state']['wtime']
                self.game_metadata['clock']['white']['increment'] = data['state']['winc']
                self.game_metadata['clock']['black']['time'] = data['state']['btime']
                self.game_metadata['clock']['black']['increment'] = data['state']['binc']

            elif 'gsd_gameState' in kwargs:
                data = kwargs['gsd_gameState']
                # NOTE: Times below come from lichess in milliseconds
                self.game_metadata['clock']['white']['time'] = data['wtime']
                self.game_metadata['clock']['black']['time'] = data['btime']
                self.game_metadata['status'] = data['status']

            self._notify_game_model_updated()
        except Exception as e:
            log.exception(f"Error saving online game metadata: {e}")
            raise

    def _subscribe_to_iem_events(self) -> None:
        """Subscribe to IEM events by adding a handler"""
        self.api_iem.e_new_event_received.add_listener(self.handle_iem_event)

    def _unsubscribe_from_iem_events(self) -> None:
        """Unsubscribe from IEM events. It's important that this happens after a game
           completes, or the user quits otherwise IEM subscriptions will build up.
        """
        self.api_iem.e_new_event_received.remove_listener(self.handle_iem_event)

    def _default_game_metadata(self) -> dict:
        """Returns the default structure for game metadata"""
        game_metadata = super()._default_game_metadata()
        game_metadata.update({
            'my_color': "",
            'ai_level': None,
            'rated': False,
            'speed': None,
        })
        return game_metadata
