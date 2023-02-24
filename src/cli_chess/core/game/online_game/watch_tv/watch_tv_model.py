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
from cli_chess.utils.logging import log
from chess import COLOR_NAMES
from berserk.exceptions import ResponseError
from time import sleep
import threading


class WatchTVModel(GameModelBase):
    def __init__(self, channel: TVChannelMenuOptions):
        super().__init__(variant=channel.variant, fen=None)
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
            if 'tv_gameStartEvent' in kwargs:
                # Reset game metadata
                self.game_metadata = self._default_game_metadata()

                data = kwargs['tv_gameStartEvent']
                self.game_metadata['gameId'] = data.get('id')
                self.game_metadata['rated'] = data.get('rated')
                self.game_metadata['variant'] = data.get('variant')
                self.game_metadata['speed'] = data.get('speed')

                for color in COLOR_NAMES:
                    if data['players'][color].get('user'):
                        self.game_metadata['players'][color] = data['players'][color]['user']
                        self.game_metadata['players'][color]['rating'] = data['players'][color]['rating']
                    elif data['players'][color].get('aiLevel'):
                        self.game_metadata['players'][color]['name'] = f"Stockfish level {data['players'][color]['aiLevel']}"

            if 'tv_coreGameEvent' in kwargs:
                data = kwargs['tv_coreGameEvent']
                self.game_metadata['clock']['white']['time'] = data['wc']  # in seconds
                self.game_metadata['clock']['white']['increment'] = 0
                self.game_metadata['clock']['black']['time'] = data['bc']  # in seconds
                self.game_metadata['clock']['black']['increment'] = 0

            if 'tv_endGameEvent' in kwargs:
                data = kwargs['tv_endGameEvent']
                self.game_metadata['state']['status'] = data.get('status')
                self.game_metadata['state']['winner'] = data.get('winner')  # Not included on draws or abort

                for color in COLOR_NAMES:
                    if data['players'][color].get('user'):
                        self.game_metadata['players'][color] = data['players'][color]['user']
                        self.game_metadata['players'][color]['rating'] = data['players'][color]['rating']
                        self.game_metadata['players'][color]['ratingDiff'] = data.get('players', {}).get(color, {}).get('ratingDiff', "")  # NOTE: Not included on aborted games # noqa
                    elif data['players'][color].get('aiLevel'):
                        self.game_metadata['players'][color]['name'] = f"Stockfish level {data['players'][color]['aiLevel']}"

            self.e_game_model_updated.notify()
        except Exception as e:
            log.error(f"TV Model: Error saving game metadata: {e}")
            raise

    def stream_event_received(self, **kwargs):
        """An event was received from the TV thread. Raises exception on invalid data"""
        try:
            # TODO: Data needs to be organized and sent to presenter to handle display
            if 'startGameEvent' in kwargs:
                event = kwargs['startGameEvent']
                variant = event['variant']['key']
                white_rating = int(event['players']['white'].get('rating') or 0)
                black_rating = int(event['players']['black'].get('rating') or 0)
                orientation = True if ((white_rating >= black_rating) or self.channel.variant.lower() == "racingkings") else False

                self._save_game_metadata(tv_gameStartEvent=event)
                last_move = event.get('lastMove', "")
                if variant == "crazyhouse" and len(last_move) == 4 and last_move[:2] == last_move[2:]:
                    # NOTE: This is a dirty fix. When streaming a crazyhouse game from lichess, if the
                    #   last move field in the initial stream output is a drop, lichess sends this as
                    #   e.g. e2e2 instead of N@e2. This causes issues parsing the UCI as e2e2 is invalid.
                    #   Considering we only use `lm` and `lastMove` for highlighting squares, this fix
                    #   changes this to a valid UCI string to still allow the square to be highlighted.
                    #   Without this, an exception will occur and we will call the API again, which is unnecessary.
                    last_move = "k@" + last_move[2:]

                self.board_model.reinitialize_board(variant, orientation, event.get('fen'), last_move)

            if 'coreGameEvent' in kwargs:
                # NOTE: the `lm` field that lichess sends is not valid UCI. It should only be used
                #       for highlighting move squares (invalid castle notation, missing promotion piece, etc).
                event = kwargs['coreGameEvent']
                self._save_game_metadata(tv_coreGameEvent=event)
                self.board_model.set_board_position(event.get('fen'), uci_last_move=event.get('lm'))

            if 'endGameEvent' in kwargs:
                event = kwargs['endGameEvent']
                self._save_game_metadata(tv_endGameEvent=event)
        except Exception as e:
            log.error(f"TV Model: Error parsing stream data: {e}")
            raise


class StreamTVChannel(threading.Thread):
    def __init__(self, channel: TVChannelMenuOptions):
        super().__init__(daemon=True)
        self.channel = channel
        self.current_game = ""
        self.running = False
        self.max_retries = 10
        self.retries = 0
        self.e_tv_stream_event = Event()

        try:
            from cli_chess.core.api.api_manager import api_client
            self.api_client = api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("StreamTVChannel: Failed to import api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

        # Current flow that has to be followed to watch the "variant" tv channels
        # as /api/tv/feed is only for the top rated game, and doesn't allow channel specification
        # 1. Get current tv game (/api/tv/channels) -> Get the game ID for the game we're interested in
        # 2. Start streaming game, on initial input set board orientation, show player names, etc. On follow up set pos.
        # 3. When the game completes, start this loop over.

    def get_channel_game_id(self, channel: str) -> str:
        """Returns the game ID of the ongoing TV game of the passed in channel"""
        channel_game_id = self.api_client.tv.get_current_games().get(channel, {}).get('gameId')
        if not channel_game_id:
            raise ValueError(f"TV Stream: Didn't receive game ID for current {channel} TV game")

        return channel_game_id

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
                    stream = self.api_client.games.stream_game_moves(game_id)

                    for event in stream:
                        # TODO: This does close the stream, but not until the next event comes in (which can be a while
                        #  sometimes (especially in longer time format games like Classical). Ideally there's
                        #  a way to immediately kill the stream, without waiting for another event. This is certainly
                        #  something to watch for since if a user backs out of multiple TV streams and immediately
                        #  enters another streams/threads will start to compound streams/threads and quickly
                        #  bring us close to the 8 streams open per IP limit.
                        if not self.running:
                            stream.close()
                            break

                        fen = event.get('fen')
                        winner = event.get('winner')
                        status = event.get('status', {}).get('name')

                        if winner or status != "started" and status:
                            log.info(f"TV Stream: Game finished: {game_id}")
                            self.e_tv_stream_event.notify(endGameEvent=event)
                            break

                        if status == "started":
                            log.info(f"TV Stream: Started streaming TV game: {game_id}")
                            self.e_tv_stream_event.notify(startGameEvent=event)
                            turns_behind = event.get('turns')

                        if fen:
                            if turns_behind and turns_behind > 0:
                                # Keeping track of turns behind allows skipping this event until
                                # we are caught up. This stops a quick game replay from happening.
                                turns_behind -= 1
                            else:
                                if event.get('wc') and event.get('bc'):
                                    self.e_tv_stream_event.notify(coreGameEvent=event)

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
