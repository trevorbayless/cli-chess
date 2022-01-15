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
from cli_chess.utils import config
import chess.engine


class EngineModel:
    def __init__(self, board_model: BoardModel):
        self.board_model = board_model
        self.engine_settings = {
            'engine_path': config.get_engine_value(config.EngineKeys.ENGINE_PATH),
            'think_time': 1.0
        }

    async def get_best_move(self) -> chess.engine.PlayResult:
        if self.engine_settings['engine_path']:
            _, engine = await chess.engine.popen_uci(self.engine_settings['engine_path'])

            return await engine.play(self.board_model.board,
                                     chess.engine.Limit(time=self.engine_settings['think_time']))
