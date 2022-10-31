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

import asyncio
from . import EngineModel
from chess.engine import PlayResult


class EnginePresenter:
    def __init__(self, engine_model: EngineModel):
        self.engine_model = engine_model

    async def get_best_move(self) -> PlayResult:
        """Notify the engine to get the best move from the current position"""
        return await self.engine_model.get_best_move()
