# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.game.board import BoardModel
from cli_chess.utils.logging import configure_logger
from cli_chess.utils.config import engine_config
import chess.engine

configure_logger("chess.engine")


async def load_engine() -> chess.engine.UciProtocol:
    """Load the chess engine"""
    engine_path = engine_config.get_value(engine_config.Keys.ENGINE_PATH)
    _, engine = await chess.engine.popen_uci(engine_path)
    return engine


class EngineModel:
    def __init__(self, engine: chess.engine.UciProtocol, board_model: BoardModel):
        self.board_model = board_model
        self.engine = engine
        self.engine_settings = {
            'engine_path': engine_config.get_value(engine_config.Keys.ENGINE_PATH),
            'think_time': 0.1
        }

    async def get_best_move(self) -> chess.engine.PlayResult:
        """Query the engine to get the best move"""
        return await self.engine.play(self.board_model.board,
                                      chess.engine.Limit(time=self.engine_settings['think_time']))
