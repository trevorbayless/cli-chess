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

from cli_chess.modules.board import BoardModel
from cli_chess.modules.move_list import MoveListModel
from cli_chess.modules.material_difference import MaterialDifferenceModel
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.utils.event import Event
from cli_chess.utils.config import lichess_config
from cli_chess.utils.logging import log
import berserk
from berserk.exceptions import ApiError, ResponseError
from time import sleep
import threading


class StreamTVChannel(threading.Thread):
    def __init__(self, channel: TVChannelMenuOptions, model, **kwargs):
        super().__init__(**kwargs)
        self.session = berserk.TokenSession(lichess_config.get_value(lichess_config.Keys.API_TOKEN))
        self.client = berserk.Client(self.session)
        self.board_model = model
        self.channel = channel.value
        self.prev_game_id = ""
        self.running = True
        self.turns_behind = 0

        # Current flow that has to be followed to watch the "variant" tv channels
        # as /api/tv/feed is only for the top rated game, and doesn't allow channel specification
        # 1. get current tv game (/api/tv/channels) -> Get the game ID for the game we're interested in
        # 2. Export the game as JSON to pull white/black names, titles, ratings, etc
        # 3. Using the data returned from #2, set board orientation, show player names, etc
        # 4. Stream the moves of the game using /api/stream/game/{id}
        # 5. When the game completes, start this loop over.

    def run(self):
        log.info(f"TV: Started watching {self.channel} TV")
        while self.running:
            try:
                game_id = self.get_channel_game_id(self.channel)

                if game_id != self.prev_game_id:
                    self.prev_game_id = game_id
                    game_metadata = self.get_game_metadata(game_id)
                    stream = self.client.games.stream_game_moves(game_id)

                    log.info(f"TV: Started streaming TV game: {game_id}")

                    for event in stream:
                        if not self.running:
                            stream.close()
                            break

                        fen = event.get('fen')
                        winner = event.get('winner')
                        status = event.get('status', {}).get('name')

                        if winner or status != "started" and status:
                            log.info(f"TV: Game end, finding next TV game.")
                            self.turns_behind = 0
                            sleep(2)
                            break

                        if status == "started":
                            log.info(f"STARTED -- {game_metadata}")
                            log.info(f"{event}")

                            white_rating = int(game_metadata.get('players', {}).get('white', {}).get('rating') or 0)
                            black_rating = int(game_metadata.get('players', {}).get('black', {}).get('rating') or 0)

                            orientation = True if white_rating >= black_rating else False

                            # TODO: If the variant is 3check the initial export fen will include the check counts
                            #       but follow up game stream FENs will not. Need to create lila api gh issue to talk
                            #       over possible solutions (including move history, etc)
                            self.board_model.set_board_position(fen, orientation, uci_last_move=event.get('lastMove'))
                            self.turns_behind = event.get('turns')

                        if fen:
                            if self.turns_behind and self.turns_behind > 0:
                                self.turns_behind -= 1
                            else:
                                self.board_model.set_board_position(fen, uci_last_move=event.get('lm'))
                else:
                    log.info("TV: Same game found, sleeping 2 seconds.")
                    sleep(2)
            except ResponseError as e:
                # TODO: Return to main menu with reason
                log.error(f"TV: ResponseError: {e}")
                log.error(f"e.message = {e.message}, e.args = {e.args}, e.reason() = {e.reason()}, e.status_code() = {e.status_code()}")
                if e.status_code() == "429":
                    log.info("TV: 429 error received, sleeping 60 seconds before retrying.")
                    sleep(60)
                else:
                    raise

            except ApiError as e:
                log.error(f"TV: ApiError: {e}")
                log.error(f"e.message = {e.message}, e.args = {e.args}, e.error = {e.error}")
                # TODO: Attempt reconnection on connect aborted:
                #  ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
                self.stop_watching()
                raise

    def get_channel_game_id(self, channel: str):
        """Returns the game ID of the ongoing TV game of the passed in channel"""
        return self.client.tv.get_current_games()[channel]['gameId']

    def get_game_metadata(self, game_id: str):
        """Return the metadata for the passed in Game ID"""
        return self.client.games.export(game_id)

    def stop_watching(self):
        self.running = False


class WatchTVModel:
    def __init__(self, channel: TVChannelMenuOptions):
        var = channel.variant
        self.board_model = BoardModel(variant=var)
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)
        self.channel = channel
        self.watching_thr = []
        self.e_watch_tv_model_updated = Event()

    def start_watching(self):
        tv_stream = StreamTVChannel(self.channel, self.board_model)
        self.watching_thr.append(tv_stream)
        tv_stream.start()

    def stop_watching(self):
        for thr in self.watching_thr:
            thr.stop_watching()
            self.watching_thr.remove(thr)

    def _notify_watch_tv_model_updated(self) -> None:
        """Notify listeners that the model has updated"""
        self.e_watch_tv_model_updated.notify()
