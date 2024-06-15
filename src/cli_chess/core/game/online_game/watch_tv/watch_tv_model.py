from cli_chess.core.game import GameModelBase
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.utils.event import Event, EventTopics
from cli_chess.utils.logging import log
from chess import COLOR_NAMES, COLORS, Color, WHITE
from berserk.exceptions import ResponseError
from time import sleep
from typing import Optional, Dict
import threading


class WatchTVModel(GameModelBase):
    def __init__(self, channel: TVChannelMenuOptions):
        super().__init__(variant=channel.variant, fen=None)
        self.channel = channel
        self._tv_stream = StreamTVChannel(self.channel)
        self._tv_stream.e_tv_stream_event.add_listener(self.stream_event_received)

    def start_watching(self):
        """Notify the TV stream thread to start"""
        self._tv_stream.start()

    def stop_watching(self):
        """Stop the TV stream thread"""
        if self._tv_stream.is_alive():
            self._tv_stream.stop_watching()

    def _update_game_metadata(self, *args, data: Optional[Dict] = None) -> None:
        """Parses and saves the data of the game being played"""
        if not data:
            return
        try:
            if EventTopics.GAME_START in args:
                self.game_metadata.reset()
                self.game_metadata.game_id = data.get('id')
                self.game_metadata.variant = self.channel

                for i, color in enumerate(COLOR_NAMES[::-1]):
                    color_as_bool = Color(COLOR_NAMES.index(color))
                    side_data = data.get('players', {})[i]
                    player_data = side_data.get('user', {})
                    ai_level = side_data.get('ai')
                    if side_data and not ai_level:
                        if player_data:
                            self.game_metadata.players[color_as_bool].title = player_data.get('title')
                            self.game_metadata.players[color_as_bool].name = player_data.get('name')
                            self.game_metadata.players[color_as_bool].rating = side_data.get('rating', "?")
                            self.game_metadata.players[color_as_bool].is_provisional_rating = side_data.get('provisional', False)
                        else:
                            self.game_metadata.players[color_as_bool].name = "Anonymous"
                    elif ai_level:
                        self.game_metadata.players[color_as_bool].name = f"Stockfish level {ai_level}"

            if EventTopics.MOVE_MADE in args:
                for color in COLORS:
                    self.game_metadata.clocks[color].units = "sec"
                    self.game_metadata.clocks[color].time = data.get('wc' if color == WHITE else 'bc')

        except Exception as e:
            log.error(f"Error saving game metadata: {e}")
            raise

    def stream_event_received(self, *args, data: Optional[Dict] = None, **kwargs):
        """An event was received from the TV thread. Raises exception on invalid data"""
        try:
            if data:
                if EventTopics.GAME_START in args:
                    orientation = Color(COLOR_NAMES.index(data.get('orientation', 'white')))
                    self.board_model.reinitialize_board(self.channel.variant, orientation, data.get('fen'))

                if EventTopics.MOVE_MADE in args:
                    # NOTE: the `lm` field that lichess sends for TV feeds and 'lastMove' field sent
                    # during game spectator streams is not valid UCI. It should only be used
                    # for highlighting move squares (invalid castle notation, missing promotion piece,
                    # crazyhouse drop notation, etc).
                    self.board_model.set_board_position(data.get('fen'), uci_last_move=data.get('lm'))

            self._update_game_metadata(*args, data=data)
            self._notify_game_model_updated(*args, **kwargs)
        except Exception as e:
            log.error(f"Error parsing stream data: {e}")
            raise


# To restore old TV streaming logic see commit 23ca5cd
class StreamTVChannel(threading.Thread):
    def __init__(self, channel: TVChannelMenuOptions):
        super().__init__(daemon=True)
        self.channel = channel
        self.running = False
        self.max_retries = 10
        self.retries = 0
        self.e_tv_stream_event = Event()

        try:
            from cli_chess.core.api.api_manager import api_client
            self.api_client = api_client
        except Exception as e:
            self.handle_exceptions(e)

    def run(self):
        """Main entrypoint for the thread"""
        log.info(f"Started watching {self.channel.value} TV")
        self.running = True
        while self.running:
            try:
                self.e_tv_stream_event.notify(EventTopics.GAME_SEARCH)

                # TODO: Update to use berserk TV specific method once implemented
                stream = self.api_client.tv._r.get(f"/api/tv/{self.channel.key}/feed", stream=True)  # noqa

                for event in stream:
                    # TODO: This does close the stream, but not until the next event comes in (which can be a while
                    #  sometimes (especially in longer time format games like Classical). Ideally there's
                    #  a way to immediately kill the stream, without waiting for another event.
                    if not self.running:
                        stream.close()
                        break

                    t = event.get('t')
                    d = event.get('d')
                    if not t or not d:
                        raise ValueError(f"Unable to stream TV as the data is malformed: {event}")

                    if t == 'featured':
                        log.info(f"Started streaming TV game: {d.get('id')}")
                        self.e_tv_stream_event.notify(EventTopics.GAME_START, data=d)

                    if t == 'fen':
                        self.e_tv_stream_event.notify(EventTopics.MOVE_MADE, data=d)

            except Exception as e:
                self.handle_exceptions(e)

            else:
                if self.running:
                    self.retries = 0
                    log.debug("Sleeping 2 seconds before finding next TV game")
                    sleep(2)

    def handle_exceptions(self, e: Exception):
        """Handles the passed in exception and responds appropriately"""
        log.error(e)
        if self.retries <= self.max_retries:
            delay = 2 * (self.retries + 1)

            if isinstance(e, ResponseError):
                if e.status_code == 429:
                    delay = 60

            log.info(f"Sleeping {delay} seconds before retrying ({self.max_retries - self.retries} retries left).")
            self.e_tv_stream_event.notify(EventTopics.ERROR, msg=f"Error streaming. Retrying in {delay} seconds.")
            sleep(delay)
            self.retries += 1
        else:
            self.e_tv_stream_event.notify(EventTopics.ERROR, msg="Retries exhausted. Stopping TV.")
            self.stop_watching()

    def stop_watching(self):
        log.info("Stopping TV stream")
        self.e_tv_stream_event.remove_all_listeners()
        self.running = False
