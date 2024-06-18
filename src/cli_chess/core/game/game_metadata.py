from dataclasses import dataclass
from chess import Color, COLORS
from typing import Optional


@dataclass
class PlayerMetadata:
    title: Optional[str] = None
    name: Optional[str] = None
    rating: Optional[str] = None
    rating_diff: Optional[int] = None
    is_provisional_rating: bool = False
    ai_level: Optional[str] = None


@dataclass
class ClockMetadata:
    units: str = "ms"
    time: Optional[int] = None
    increment: Optional[int] = None
    ticking: bool = False


@dataclass
class GameStatusMetadata:
    status: Optional[str] = None
    winner: Optional[str] = None


class GameMetadata:
    def __init__(self):
        self.players = [PlayerMetadata(), PlayerMetadata()]
        self.clocks = [ClockMetadata(), ClockMetadata()]
        self.game_status = GameStatusMetadata()
        self.game_id: Optional[str] = None
        self.variant: Optional[str] = None
        self.my_color: Optional[Color] = None
        self.rated: bool = False
        self.speed: Optional[str] = None

    def set_clock_ticking(self, color: Optional[Color]):
        if color is None:
            for c in COLORS:
                self.clocks[c].ticking = False
        else:
            self.clocks[color].ticking = True
            self.clocks[not color].ticking = False

    def reset(self):
        self.__init__()
