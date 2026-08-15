from cli_chess.core.game import GameModelBase
from cli_chess.utils.pgn import build_pgn_game, save_game_pgn
from berserk.utils import datetime_from_millis
from chess import WHITE, BLACK
import chess.pgn
import pytest


@pytest.fixture
def model():
    model = GameModelBase()
    model.board_model.make_move("e4")
    model.board_model.make_move("e5")
    model.game_metadata.players[WHITE].name = "testWhite"
    model.game_metadata.players[BLACK].name = "testBlack"
    model.game_metadata.game_status.status = "resign"
    model.game_metadata.game_status.winner = "white"
    return model


def set_online_clocks(model: GameModelBase, time, increment, initial_time=None):
    for color in (WHITE, BLACK):
        model.game_metadata.clocks[color].units = "ms"
        model.game_metadata.clocks[color].time = time
        model.game_metadata.clocks[color].increment = increment
        model.game_metadata.clocks[color].initial_time = initial_time if initial_time is not None else time


def test_time_control_header_with_datetime_clocks(model: GameModelBase):
    """Berserk converts wtime/btime/winc/binc to datetime objects (see berserk models.GameState)"""
    set_online_clocks(model, time=datetime_from_millis(180000), increment=datetime_from_millis(2000))
    assert build_pgn_game(model.board_model, model.game_metadata, is_online=True).headers["TimeControl"] == "180+2"


def test_time_control_header_with_millisecond_clocks(model: GameModelBase):
    set_online_clocks(model, time=180000, increment=2000)
    assert build_pgn_game(model.board_model, model.game_metadata, is_online=True).headers["TimeControl"] == "180+2"


def test_time_control_header_uses_initial_time(model: GameModelBase):
    """The clock time is overwritten with the remaining time as moves are made"""
    set_online_clocks(model, time=37000, increment=2000, initial_time=180000)
    assert build_pgn_game(model.board_model, model.game_metadata, is_online=True).headers["TimeControl"] == "180+2"


def test_time_control_header_without_clocks(model: GameModelBase):
    assert build_pgn_game(model.board_model, model.game_metadata, is_online=False).headers["TimeControl"] == "-"


def test_save_game_pgn_saves_online_game(model: GameModelBase, monkeypatch, tmp_path):
    monkeypatch.setattr("cli_chess.utils.pgn.get_pgn_save_dir", lambda: str(tmp_path))
    set_online_clocks(model, time=datetime_from_millis(37000), increment=datetime_from_millis(2000), initial_time=datetime_from_millis(180000))  # noqa: E501
    model.game_metadata.game_id = "testGameId"

    path = save_game_pgn(model.board_model, model.game_metadata, is_online=True)

    assert path is not None
    with open(path, encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
    assert game.headers["Site"] == "lichess.org/testGameId"
    assert game.headers["TimeControl"] == "180+2"
    assert game.headers["Result"] == "1-0"
    assert [move.uci() for move in game.mainline_moves()] == ["e2e4", "e7e5"]


def test_save_game_pgn_skips_game_without_moves(monkeypatch, tmp_path):
    monkeypatch.setattr("cli_chess.utils.pgn.get_pgn_save_dir", lambda: str(tmp_path))
    model = GameModelBase()

    assert save_game_pgn(model.board_model, model.game_metadata, is_online=False) is None
    assert not list(tmp_path.iterdir())
