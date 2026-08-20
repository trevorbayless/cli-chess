from __future__ import annotations
from cli_chess.modules.clock import ClockView
from cli_chess.utils import EventTopics, log
from chess import Color
from datetime import datetime, timedelta, timezone
from time import monotonic
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase


class ClockPresenter:
    def __init__(self, model: GameModelBase):
        self.model = model

        self.view_upper = ClockView(self, lambda: self.get_clock_display(not self.model.board_model.get_board_orientation()))
        self.view_lower = ClockView(self, lambda: self.get_clock_display(self.model.board_model.get_board_orientation()))

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, *args, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        if (EventTopics.GAME_START in args or EventTopics.GAME_END in args or
                EventTopics.MOVE_MADE in args or EventTopics.BOARD_ORIENTATION_CHANGED in args):
            orientation = self.model.board_model.get_board_orientation()
            self.view_upper.update(self.model.game_metadata.clocks[not orientation].ticking)
            self.view_lower.update(self.model.game_metadata.clocks[orientation].ticking)

    def get_clock_display(self, color: Color) -> str:
        """Returns the formatted clock display for the color passed in"""
        clock_data = self.model.game_metadata.clocks[color]
        time = clock_data.time

        if time is None:
            return "--:--"

        try:
            if not isinstance(time, datetime):
                if isinstance(time, timedelta):
                    seconds = time.total_seconds()
                else:
                    seconds = float(time) / 1000 if clock_data.units == "ms" else float(time)

                time = datetime.fromtimestamp(seconds, timezone.utc)

            if clock_data.ticking and clock_data.tick_started_at is not None:
                elapsed = monotonic() - clock_data.tick_started_at
                time = max(datetime.fromtimestamp(0, timezone.utc), time - timedelta(seconds=elapsed))

            return time.strftime("%M:%S") if not time.hour else time.strftime("%H:%M:%S")
        except Exception as e:
            log.error(f"Error formatting clock display for color {color}: {e}")
            return "--:--"
