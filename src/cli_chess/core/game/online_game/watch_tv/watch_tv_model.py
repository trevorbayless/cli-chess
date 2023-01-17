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
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.utils.event import Event
from cli_chess.utils.config import lichess_config
from cli_chess.utils.logging import log
from berserk.exceptions import ResponseError
import berserk
from time import sleep
import threading


class WatchTVModel(GameModelBase):
    def __init__(self, channel: TVChannelMenuOptions):
        super().__init__(variant=channel.variant)
        self.channel = channel
        self._tv_stream = StreamTVChannel(self.channel)

        self.e_watch_tv_model_updated = Event()
        self._tv_stream.e_tv_stream_event.add_listener(self.stream_event_received)

    def start_watching(self):
        """Notify the TV stream thread to start"""
        log.info(f"TV Model: Starting TV stream")
        self._tv_stream.start()

    def stop_watching(self):
        """Stop the TV stream thread"""
        if self._tv_stream.is_alive():
            log.info("TV Model: Stopping TV stream")
            self._tv_stream.stop_watching()

    def stream_event_received(self, **kwargs):
        """An event was received from the TV thread"""
        # TODO: Data needs to be organized and sent to presenter to handle display
        if '_startGameEvent' in kwargs and '_gameMetadata' in kwargs:
            game_metadata = kwargs['_gameMetadata']
            event = kwargs['_startGameEvent']
            white_rating = int(game_metadata.get('players', {}).get('white', {}).get('rating') or 0)
            black_rating = int(game_metadata.get('players', {}).get('black', {}).get('rating') or 0)
            orientation = True if ((white_rating >= black_rating) or self.channel.variant.lower() == "racingkings") else False

            # TODO: If the variant is 3check the initial export fen will include the check counts
            #       but follow up game stream FENs will not. Need to create lila api gh issue to talk
            #       over possible solutions (including move history, etc)
            self.board_model.set_board_position(event.get('fen'), orientation, uci_last_move=event.get('lastMove'))

        if '_coreGameEvent' in kwargs:
            event = kwargs['_coreGameEvent']
            self.board_model.set_board_position(event.get('fen'), uci_last_move=event.get('lm'))

        if '_endGameEvent' in kwargs:
            event = kwargs['_endGameEvent']

    def _notify_watch_tv_model_updated(self) -> None:
        """Notify listeners that the model has updated"""
        self.e_watch_tv_model_updated.notify()


class StreamTVChannel(threading.Thread):
    def __init__(self, channel: TVChannelMenuOptions, **kwargs):
        super().__init__(**kwargs)
        self.session = berserk.TokenSession(lichess_config.get_value(lichess_config.Keys.API_TOKEN))
        self.client = berserk.Client(self.session)
        self.channel = channel
        self.current_game = ""
        self.connection_retries = 10
        self.running = False
        self.e_tv_stream_event = Event()

        # Current flow that has to be followed to watch the "variant" tv channels
        # as /api/tv/feed is only for the top rated game, and doesn't allow channel specification
        # 1. get current tv game (/api/tv/channels) -> Get the game ID for the game we're interested in
        # 2. Export the game as JSON to pull white/black names, titles, ratings, etc
        # 3. Using the data returned from #2, set board orientation, show player names, etc
        # 4. Stream the moves of the game using /api/stream/game/{id}
        # 5. When the game completes, start this loop over.

    def get_channel_game_id(self, channel: str):
        """Returns the game ID of the ongoing TV game of the passed in channel"""
        return self.client.tv.get_current_games()[channel]['gameId']

    def get_game_metadata(self, game_id: str):
        """Return the metadata for the passed in Game ID"""
        return self.client.games.export(game_id)

    def stop_watching(self):
        self.running = False

    def run(self):
        """Main entrypoint for the thread"""
        log.info(f"TV Stream: Started watching {self.channel.value} TV")
        self.running = True
        # TODO: Need to handle going back to the main menu if the TVStream connection retries are exhausted
        while self.running and self.connection_retries > 0:
            try:
                game_id = self.get_channel_game_id(self.channel.value)

                if game_id != self.current_game:
                    self.current_game = game_id
                    turns_behind = 0
                    game_metadata = self.get_game_metadata(game_id)
                    stream = self.client.games.stream_game_moves(game_id)

                    for event in stream:
                        if not self.running:
                            stream.close()
                            break

                        fen = event.get('fen')
                        winner = event.get('winner')
                        status = event.get('status', {}).get('name')

                        if winner or status != "started" and status:
                            log.info(f"TV Stream: Game finished: {game_id}")
                            self.e_tv_stream_event.notify(_endGameEvent=event)
                            break

                        if status == "started":
                            log.info(f"TV Stream: Started streaming TV game: {game_id}")
                            self.e_tv_stream_event.notify(_gameMetadata=game_metadata, _startGameEvent=event)
                            turns_behind = event.get('turns')

                        if fen:
                            if turns_behind and turns_behind > 0:
                                # Keeping track of turns behind allows skipping this event until
                                # we are caught up. This stops a quick game replay from happening.
                                turns_behind -= 1
                            else:
                                self.e_tv_stream_event.notify(_coreGameEvent=event)

            except Exception as e:
                self.handle_exceptions(e)

            else:
                if self.running:
                    self.connection_retries = 10
                    log.info("TV Stream: Sleeping 2 seconds before finding next TV game")
                    sleep(2)

    def handle_exceptions(self, e: Exception):
        """Handles the passed in exception and responds appropriately"""
        log.error(f"TV Stream: {e}")
        self.connection_retries -= 1
        self.current_game = ""
        delay = 5

        if isinstance(e, ResponseError):
            if e.status_code == 429:
                delay = 60

        log.info(f"TV Stream: Sleeping {delay} seconds before retrying ({self.connection_retries} retries left).")
        sleep(delay)
