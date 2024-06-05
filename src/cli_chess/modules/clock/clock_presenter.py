from __future__ import annotations
from cli_chess.modules.clock import ClockView
from chess import Color
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
        clock_data = self.model.game_metadata.clocks[color]
        time = clock_data.time

        if not time:
            return "--:--"

        if not isinstance(time, datetime):
            if clock_data.units == "ms":
                time = datetime.fromtimestamp(time / 1000, timezone.utc)
            elif clock_data.units == "sec":
                time = datetime.fromtimestamp(time, timezone.utc)

        return time.strftime("%M:%S") if not time.hour else time.strftime("%H:%M:%S")
