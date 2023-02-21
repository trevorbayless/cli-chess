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

from cli_chess.utils import Event, log
import threading


class GameStateDispatcher(threading.Thread):
    """Handles streaming a game and sending game commands (make move, offer draw, etc)
       using the Board API. The game that is streamed using this class must be owned
       by the account linked to the api token.
    """

    def __init__(self, game_id=""):
        super().__init__()
        self.game_id = game_id
        self.e_game_state_dispatcher_event = Event()

        try:
            from cli_chess.core.api.api_manager import api_client
            self.api_client = api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("GameStateDispatcher: Failed to import api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

    def run(self):
        """This is the threads main function. It handles emitting the game state to
           listeners (typically the OnlineGameModel).
        """
        log.info(f"GameStateDispatcher: Started streaming game state: {self.game_id}")

        for event in self.api_client.board.stream_game_state(self.game_id):
            if event['type'] == "gameFull":
                self.e_game_state_dispatcher_event.notify(gameFull=event)

            elif event['type'] == "gameState":
                self.e_game_state_dispatcher_event.notify(gameState=event)
                is_game_over = event.get('winner')
                if is_game_over:
                    break

            elif event['type'] == "chatLine":
                self.e_game_state_dispatcher_event.notify(chatLine=event)

            elif event['type'] == "opponentGone":
                # TODO: Start countdown if opponent is gone. Automatically claim win if timer elapses.
                #  The countdown should stop if the opponent comes back before the timer elapses.
                self.e_game_state_dispatcher_event.notify(opponentGone=event)

        log.info(f"GameStateDispatcher: Completed streaming of: {self.game_id}")

    def make_move(self, move: str):
        """Sends the move to lichess. This move should have already
           been verified as valid in the current context of the board.
           The move must be in UCI format.
        """
        try:
            log.debug(f"GameStateDispatcher: Sending move ({move}) to lichess")
            self.api_client.board.make_move(self.game_id, move)
        except Exception:
            raise

    def send_takeback_request(self) -> None:
        """Sends a takeback request to our opponent"""
        try:
            log.debug(f"GameStateDispatcher: Sending takeback offer to opponent")
            self.api_client.board.offer_takeback(self.game_id)
        except Exception:
            raise

    def send_draw_offer(self) -> None:
        """Sends a draw offer to our opponent"""
        try:
            log.debug(f"GameStateDispatcher: Sending draw offer to opponent")
            self.api_client.board.offer_draw(self.game_id)
        except Exception:
            raise

    def resign(self) -> None:
        """Resigns the game"""
        try:
            log.debug(f"GameStateDispatcher: Sending resignation")
            self.api_client.board.resign_game(self.game_id)
        except Exception:
            raise

    def clear_listeners(self) -> None:
        """Remove all event listeners"""
        self.e_game_state_dispatcher_event.listeners.clear()
