from cli_chess.core.game import game_presenter_base
from cli_chess.core.game.game_options import GameOption
from cli_chess.core.game.offline_game import OfflineGameModel, OfflineGamePresenter
from cli_chess.utils import EventTopics
from cli_chess.utils.pgn import save_game_pgn
from chess import WHITE
from unittest.mock import Mock
import pytest


@pytest.fixture
def save_spy(monkeypatch, tmp_path):
    from cli_chess.utils import pgn
    monkeypatch.setattr(pgn, "get_pgn_save_dir", lambda: str(tmp_path))
    spy = Mock(wraps=save_game_pgn)
    monkeypatch.setattr(game_presenter_base, "save_game_pgn", spy)
    return spy


@pytest.fixture
def presenter(monkeypatch, save_spy):
    from cli_chess.core.game.offline_game import offline_game_model
    monkeypatch.setattr(offline_game_model, "EngineModel", Mock())

    game_parameters = {
        GameOption.COLOR: "white",
        GameOption.VARIANT: "standard",
        GameOption.COMPUTER_SKILL_LEVEL: 1,
        GameOption.SPECIFY_ELO: False,
        GameOption.COMPUTER_ELO: 1500,
    }
    return OfflineGamePresenter(OfflineGameModel(game_parameters))


def saved_lines(presenter) -> list:
    return [line for line in presenter.view.alert._alert_label.text.split("\n") if line.startswith("Game saved:")]


def test_resignation_saves_pgn_once(presenter, save_spy, tmp_path):
    presenter.model.board_model.make_move("e4")
    presenter.model.board_model.handle_resignation(WHITE)

    assert save_spy.call_count == 1
    assert len(saved_lines(presenter)) == 1
    assert len(list(tmp_path.iterdir())) == 1


def test_checkmate_saves_pgn_once_and_keeps_result(presenter, save_spy, tmp_path):
    for move in ("f3", "e5", "g4", "Qh4"):
        presenter.model.board_model.make_move(move)

    assert save_spy.call_count == 1
    assert len(saved_lines(presenter)) == 1
    assert len(list(tmp_path.iterdir())) == 1
    assert "Checkmate" in presenter.view.alert._alert_label.text


def test_game_start_allows_the_next_game_to_save(presenter, save_spy):
    presenter.model.board_model.make_move("e4")
    presenter.model.board_model.handle_resignation(WHITE)
    save_spy.reset_mock()

    presenter.model._notify_game_model_updated(EventTopics.GAME_START)
    presenter.model._notify_game_model_updated(EventTopics.GAME_END)

    assert save_spy.call_count == 1
    assert len(saved_lines(presenter)) == 1
