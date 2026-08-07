from cli_chess.core.game import GameModelBase
from cli_chess.modules.clock import ClockPresenter
from chess import WHITE, BLACK
from datetime import datetime, timezone
import pytest


@pytest.fixture
def model():
    return GameModelBase()


@pytest.fixture
def presenter(model: GameModelBase):
    return ClockPresenter(model)


@pytest.fixture
def fake_time(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("cli_chess.core.game.game_metadata.monotonic", lambda: now[0])
    monkeypatch.setattr("cli_chess.modules.clock.clock_presenter.monotonic", lambda: now[0])
    return now


def test_ticking_ms_clock_decrements(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = 60000
    model.game_metadata.set_clock_ticking(WHITE)
    assert presenter.get_clock_display(WHITE) == "01:00"

    fake_time[0] += 5.0
    assert presenter.get_clock_display(WHITE) == "00:55"


def test_non_ticking_clock_is_frozen(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[BLACK].units = "ms"
    model.game_metadata.clocks[BLACK].time = 60000
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 30.0
    assert presenter.get_clock_display(BLACK) == "01:00"


def test_ticking_clock_floors_at_zero(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = 3000
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 10.0
    assert presenter.get_clock_display(WHITE) == "00:00"


def test_missing_time_renders_placeholder(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].time = None
    assert presenter.get_clock_display(WHITE) == "--:--"

    model.game_metadata.set_clock_ticking(WHITE)
    fake_time[0] += 5.0
    assert presenter.get_clock_display(WHITE) == "--:--"


def test_ticking_sec_clock_decrements(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "sec"
    model.game_metadata.clocks[WHITE].time = 90
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 30.0
    assert presenter.get_clock_display(WHITE) == "01:00"


def test_game_end_freezes_both_clocks(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = 60000
    model.game_metadata.clocks[BLACK].units = "ms"
    model.game_metadata.clocks[BLACK].time = 30000
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 5.0
    model.game_metadata.set_clock_ticking(None)

    fake_time[0] += 60.0
    assert presenter.get_clock_display(WHITE) == "01:00"
    assert presenter.get_clock_display(BLACK) == "00:30"


def test_ticking_datetime_clock_decrements(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    # berserk converts the top level wtime/btime of a `gameState` event into datetimes
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = datetime.fromtimestamp(60, timezone.utc)
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 5.0
    assert presenter.get_clock_display(WHITE) == "00:55"


def test_ticking_datetime_clock_floors_at_zero(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = datetime.fromtimestamp(3, timezone.utc)
    model.game_metadata.set_clock_ticking(WHITE)

    fake_time[0] += 10.0
    assert presenter.get_clock_display(WHITE) == "00:00"


def test_hour_formatting_preserved(model: GameModelBase, presenter: ClockPresenter, fake_time: list):
    model.game_metadata.clocks[WHITE].units = "ms"
    model.game_metadata.clocks[WHITE].time = 3_660_000
    assert presenter.get_clock_display(WHITE) == "01:01:00"
