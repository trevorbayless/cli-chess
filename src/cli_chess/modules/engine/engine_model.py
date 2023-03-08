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
from cli_chess.core.game.game_options import GameOption
from cli_chess.utils import log, is_linux_os, is_windows_os
import chess.engine
from os import path

ENGINE_PATH = path.dirname(path.realpath(__file__)) + "/binaries/"
ENGINE_BINARY_NAME = "fairy-stockfish_14_x86-64_" + ("linux" if is_linux_os() else ("windows" if is_windows_os() else "mac"))

fairy_stockfish_mapped_skill_levels = {
    # These defaults are for the Fairy Stockfish engine
    # correlates levels 1-8 to a fairy-stockfish "equivalent"
    # This skill level mapping is to match Lichess' implementation
    1: -9,
    2: -5,
    3: -1,
    4: 3,
    5: 7,
    6: 11,
    7: 16,
    8: 20,
}


async def create_engine_model(board_model: BoardModel, game_parameters: dict):
    """Create an instance of the engine model with the engine loaded"""
    model = EngineModel(board_model, game_parameters)
    await model._init()  # noqa
    return model


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
        # TODO: Add support for other engines. Menu logic would need to be
        #       Updated to show only valid variants for the engine, UCI Elo levels, etc.
        try:
            _, engine = await chess.engine.popen_uci(ENGINE_PATH + ENGINE_BINARY_NAME)
            return engine
        except Exception as e:
            log.critical(f"Exception caught starting engine: {e}")
            raise e

    async def quit_engine(self) -> None:
        """Notify the engine to quit"""
        await self.engine.quit()

    async def configure_engine(self) -> None:
        """Configure the engine with the passed in options"""
        skill_level = fairy_stockfish_mapped_skill_levels.get(self.game_parameters.get(GameOption.COMPUTER_SKILL_LEVEL))
        limit_strength = self.game_parameters.get(GameOption.SPECIFY_ELO)
        uci_elo = self.game_parameters.get(GameOption.COMPUTER_ELO)

        engine_cfg = {
            'Skill Level': skill_level if skill_level else 0,
            'UCI_LimitStrength': True if limit_strength else False,
            'UCI_Elo': uci_elo if uci_elo else 1350
        }

        await self.engine.configure(engine_cfg)

    async def get_best_move(self) -> chess.engine.PlayResult:
        """Query the engine to get the best move"""
        # Keep track of the last move that was made. This allows checking
        # for if a takeback happened while the engine has been thinking
        # TODO: look into ways to cancel thinking if a takeback occurred
        last_move = (self.board_model.get_move_stack() or [None])[-1]
        result = await self.engine.play(self.board_model.board,
                                        chess.engine.Limit(2))

        # Check if the move stack has been altered, if so void this move
        if last_move != (self.board_model.get_move_stack() or [None])[-1]:
            result.move = None

        # Check to make sure the game is still in progress (opponent hasn't resigned)
        if self.board_model.get_game_over_result() is not None:
            result.move = None

        return result
