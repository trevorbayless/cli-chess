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

from cli_chess.modules.board import BoardModel
from cli_chess.utils.logging import configure_logger
from cli_chess.utils.config import engine_config
import chess.engine

engine_log = configure_logger("chess.engine")


async def create_engine_model(board_model: BoardModel, game_parameters: dict):
    """Create an instance of the engine model with the engine loaded"""
    engine_model = EngineModel(board_model, game_parameters)
    await engine_model._init()
    return engine_model


class EngineModel:
    def __init__(self, board_model: BoardModel, game_parameters: dict):
        self.board_model = board_model
        self.game_parameters = game_parameters

    async def _init(self):
        self.engine = await self.load_engine()
        await self.configure_engine()

    @staticmethod
    async def load_engine() -> chess.engine.UciProtocol:
        """Load the chess engine"""
        engine_path = engine_config.get_value(engine_config.Keys.ENGINE_PATH)
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            return engine
        except Exception as e:
            engine_log.critical(f"Exception caught starting engine: {e}")
            raise e

    async def configure_engine(self) -> None:
        """Configure the engine with the passed in options"""
        await self.engine.configure({"Skill Level": self.game_parameters['Computer Level']})  # TODO: Update 'Computer Strength' to use options enum

    async def get_best_move(self) -> chess.engine.PlayResult:
        """Query the engine to get the best move"""
        return await self.engine.play(self.board_model.board,
                                      chess.engine.Limit(2))
