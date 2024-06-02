from dataclasses import dataclass


@dataclass
class Player:
    title: str = None
    name: str = None
    rating: str = None
    rating_diff: int = None
    is_provisional_rating: bool = False


@dataclass
class Clock:
    units: str = "ms"
    time: int = 0
    increment: int = 0


@dataclass
class GameStatus:
    status: str = None
    winner: str = None


@dataclass
class GameMetadata:
    players = [Player(), Player()]
    clocks = [Clock(), Clock()]
    game_status = GameStatus()
    game_id: str = None
    variant: str = None
    my_color: str = None
