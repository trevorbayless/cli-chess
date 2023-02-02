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

    def run(self):
        from cli_chess.core.api.api_manager import api_client
        log.info(f"GameStateDispatcher: Started streaming game state: {self.game_id}")

        for event in api_client.board.stream_game_state(self.game_id):
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
                self.e_game_state_dispatcher_event.notify(opponentGone=event)

        log.info(f"GameStateDispatcher: Completed streaming of: {self.game_id}")
