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
        self._tv_stream.e_tv_stream_event.add_listener(self.stream_event_received)

    def _default_game_metadata(self) -> dict:
        """Returns the default structure for game metadata"""
        game_metadata = super()._default_game_metadata()
        game_metadata.update({
            'rated': None,
            'speed': None,
        })
        return game_metadata

    def start_watching(self):
        """Notify the TV stream thread to start"""
        self._tv_stream.start()

    def stop_watching(self):
        """Stop the TV stream thread"""
        if self._tv_stream.is_alive():
            self._tv_stream.stop_watching()

    def _save_game_metadata(self, **kwargs) -> None:
        """Parses and saves the data of the game being played"""
        try:
            if '_gameMetadata' in kwargs:
                data = kwargs['_gameMetadata']
                self.game_metadata['gameId'] = data.get('id')
                self.game_metadata['rated'] = data.get('rated')
                self.game_metadata['variant'] = data.get('variant')
                self.game_metadata['speed'] = data.get('speed')
                self.game_metadata['players']['white'] = data['players']['white']['user']
                self.game_metadata['players']['white']['rating'] = data['players']['white']['rating']
                self.game_metadata['players']['black'] = data['players']['black']['user']
                self.game_metadata['players']['black']['rating'] = data['players']['black']['rating']

            if '_coreGameEvent' in kwargs:
                data = kwargs['_coreGameEvent']
                self.game_metadata['clock']['white']['time'] = data['wc']  # in seconds
                self.game_metadata['clock']['white']['increment'] = 0
                self.game_metadata['clock']['black']['time'] = data['bc']  # in seconds
                self.game_metadata['clock']['black']['increment'] = 0

            if '_endGameEvent' in kwargs:
                data = kwargs['_endGameEvent']
                self.game_metadata['status'] = data['status']
                self.game_metadata['winner'] = data.get('winner')  # Not included on draws

            self.e_game_model_updated.notify()
        except Exception as e:
            log.error(f"TV Model: Error saving game metadata: {e}")
            raise

    def stream_event_received(self, **kwargs):
        """An event was received from the TV thread. Raises exception on invalid data"""
        try:
            # TODO: Data needs to be organized and sent to presenter to handle display
            if '_startGameEvent' in kwargs and '_gameMetadata' in kwargs:
                game_metadata = kwargs['_gameMetadata']
                event = kwargs['_startGameEvent']
                white_rating = int(game_metadata['players']['white']['rating'] or 0)
                black_rating = int(game_metadata['players']['black']['rating'] or 0)
                orientation = True if (
                            (white_rating >= black_rating) or self.channel.variant.lower() == "racingkings") else False

                self._save_game_metadata(_gameMetadata=game_metadata)
                # TODO: If the variant is 3check the initial export fen will include the check counts
                #       but follow up game stream FENs will not. Need to create lila api gh issue to talk
                #       over possible solutions (including move history, etc)
                self.board_model.set_board_position(event.get('fen'), orientation, uci_last_move=event.get('lastMove'))

            if '_coreGameEvent' in kwargs:
                event = kwargs['_coreGameEvent']
                self._save_game_metadata(_coreGameEvent=event)
                self.board_model.set_board_position(event.get('fen'), uci_last_move=event.get('lm'))

            if '_endGameEvent' in kwargs:
                event = kwargs['_endGameEvent']
                self._save_game_metadata(_endGameEvent=event)
        except Exception as e:
            log.error(f"TV Model: Error parsing stream data: {e}")
            raise


class StreamTVChannel(threading.Thread):
    def __init__(self, channel: TVChannelMenuOptions, **kwargs):
        super().__init__(**kwargs)
        self.daemon = True  # NOTE: This is only here since when exiting the program and watching a longer game (eg. classical)
                            #       the thread remained open. Remove this if a better way of closing the stream is found.
        self.session = berserk.TokenSession(lichess_config.get_value(lichess_config.Keys.API_TOKEN))
        self.client = berserk.Client(self.session)
        self.channel = channel
        self.current_game = ""
        self.running = False
        self.max_retries = 10
        self.retries = 0
        self.e_tv_stream_event = Event()

        # Current flow that has to be followed to watch the "variant" tv channels
        # as /api/tv/feed is only for the top rated game, and doesn't allow channel specification
        # 1. get current tv game (/api/tv/channels) -> Get the game ID for the game we're interested in
        # 2. Export the game as JSON to pull white/black names, titles, ratings, etc
        # 3. Using the data returned from #2, set board orientation, show player names, etc
        # 4. Stream the moves of the game using /api/stream/game/{id}
        # 5. When the game completes, start this loop over.

    def get_channel_game_id(self, channel: str) -> str:
        """Returns the game ID of the ongoing TV game of the passed in channel"""
        channel_game_id = self.client.tv.get_current_games().get(channel, {}).get('gameId')
        if not channel_game_id:
            raise ValueError(f"TV Stream: Didn't receive game ID for current {channel} TV game")

        return channel_game_id

    def get_game_metadata(self, game_id: str):
        """Return the metadata for the passed in Game ID"""
        game_metadata = self.client.games.export(game_id)
        if not game_metadata:
            raise ValueError("TV Stream: Didn't receive game metadata for current TV game")

        return game_metadata

    def run(self):
        """Main entrypoint for the thread"""
        log.info(f"TV Stream: Started watching {self.channel.value} TV")
        self.running = True
        while self.running:
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
                                if event.get('wc') and event.get('bc'):
                                    self.e_tv_stream_event.notify(_coreGameEvent=event)

            except Exception as e:
                self.handle_exceptions(e)

            else:
                if self.running:
                    self.retries = 0
                    log.debug("TV Stream: Sleeping 2 seconds before finding next TV game")
                    sleep(2)

    def handle_exceptions(self, e: Exception):
        """Handles the passed in exception and responds appropriately"""
        if self.retries <= self.max_retries:
            log.error(f"TV Stream: {e}")
            self.current_game = ""
            delay = 2 * (self.retries + 1)

            if isinstance(e, ResponseError):
                if e.status_code == 429:
                    delay = 60

            # TODO: Send event to model with retry notification so we can display it to the user
            log.info(
                f"TV Stream: Sleeping {delay} seconds before retrying ({self.max_retries - self.retries} retries left).")
            sleep(delay)
            self.retries += 1
        else:
            self.stop_watching()

    def stop_watching(self):
        # TODO: Need to handle going back to the main menu when the TVStream
        #       connection retries are exhausted. Send event notification to model?
        log.info("TV Stream: Stopping TV stream")
        self.running = False
