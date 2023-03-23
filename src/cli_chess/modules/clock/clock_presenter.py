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

from __future__ import annotations
from cli_chess.modules.clock import ClockView
from cli_chess.utils.logging import log
from chess import Color, COLOR_NAMES
from datetime import datetime, timezone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase


class ClockPresenter:
    def __init__(self, model: GameModelBase):
        self.model = model

        orientation = self.model.board_model.get_board_orientation()
        self.view_upper = ClockView(self, self.get_clock_display(not orientation))
        self.view_lower = ClockView(self, self.get_clock_display(orientation))

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        if 'boardOrientationChanged' in kwargs or 'successfulMoveMade' in kwargs or 'onlineGameOver' in kwargs or 'tvPositionUpdated' in kwargs:
            orientation = self.model.board_model.get_board_orientation()
            self.view_upper.update(self.get_clock_display(not orientation))
            self.view_lower.update(self.get_clock_display(orientation))

    def get_clock_display(self, color: Color) -> str:
        """Returns the formatted clock display for the color passed in"""
        clock_data = self.model.game_metadata.get('clock')
        units = clock_data.get('units')
        time = clock_data.get(COLOR_NAMES[color]).get('time')

        if not time:
            log.error(f"Time data is not available for {COLOR_NAMES[color]}")
            return "--:--"

        if not isinstance(time, datetime):
            if clock_data.get('units') == "ms":
                time = datetime.fromtimestamp(time / 1000, timezone.utc)
            elif units == "sec":
                time = datetime.fromtimestamp(time, timezone.utc)

        return time.strftime("%M:%S") if not time.hour else time.strftime("%H:%M:%S")
