from cli_chess.modules.material_difference import MaterialDifferenceModel, MaterialDifferencePresenter
from cli_chess.modules.board import BoardModel
from cli_chess.utils.config import GameConfig
from chess import WHITE, BLACK
from os import remove
from unittest.mock import Mock
import pytest


@pytest.fixture
def model():
    return MaterialDifferenceModel(BoardModel())


@pytest.fixture
def presenter(model: MaterialDifferenceModel, game_config: GameConfig, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.material_difference.material_difference_presenter.game_config', game_config)
    return MaterialDifferencePresenter(model)


@pytest.fixture
def game_config():
    game_config = GameConfig("unit_test_config.ini")
    yield game_config
    remove(game_config.full_filename)


def test_update(model: MaterialDifferenceModel, presenter: MaterialDifferencePresenter, game_config: GameConfig):
    # Verify the update method is listening to model updates
    assert presenter.update in model.e_material_difference_model_updated.listeners

    # Verify the update method is listening to game configuration updates
    assert presenter.update in game_config.e_game_config_updated.listeners

    # Verify the presenter update function is calling the material difference
    # views (white/black) and with the proper data
    model.board_model.set_fen("6Q1/1P2P3/4n1B1/2b3n1/KNP3p1/5k2/2pq3P/1N6 w - - 0 1")
    presenter.view_upper.update = Mock()
    presenter.view_lower.update = Mock()
    view_upper_data = presenter.format_diff_output(BLACK)
    view_lower_data = presenter.format_diff_output(WHITE)
    presenter.update()
    presenter.view_upper.update.assert_called_with(view_upper_data)
    presenter.view_lower.update.assert_called_with(view_lower_data)


def test_format_diff_output(model: MaterialDifferenceModel, presenter: MaterialDifferencePresenter, game_config: GameConfig):
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == ""
    game_config.set_value(game_config.Keys.PAD_UNICODE, "no")

    # Test white advantage
    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "yes")
    model.board_model.set_fen("1Q1B1K2/p3p3/p1PN4/p3q3/3N3k/pB6/P2r4/8 w - - 0 1")
    assert presenter.format_diff_output(WHITE) == "♝♝♞♞+4"
    assert presenter.format_diff_output(BLACK) == "♜♙♙♙"

    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "no")
    assert presenter.format_diff_output(WHITE) == "BBNN+4"
    assert presenter.format_diff_output(BLACK) == "RPPP"

    # Test black advantage
    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "yes")
    model.board_model.set_fen("3n4/1p4P1/1b1Kp3/1p1P2P1/1P1P2pk/1p6/pr6/8 w - - 0 1")
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == "♜♝♞♙+12"

    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "no")
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == "RBNP+12"

    # Test no advantage
    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "yes")
    model.board_model.set_fen("r1bqk2r/pppp1ppp/2n5/2b1p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    assert presenter.format_diff_output(WHITE) == "♞"
    assert presenter.format_diff_output(BLACK) == "♝"

    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "no")
    assert presenter.format_diff_output(WHITE) == "N"
    assert presenter.format_diff_output(BLACK) == "B"

    # Test 3check output
    model = MaterialDifferenceModel(BoardModel(fen="8/1P2N2P/1P5N/5p2/bB1k4/K1n4P/4B1pr/6R1 b - - 0 1", variant="3check"))
    presenter = MaterialDifferencePresenter(model)
    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "yes")
    assert presenter.format_diff_output(WHITE) == "♝♞♙♙+8"
    assert presenter.format_diff_output(BLACK) == ""
    model.board_model.make_move("Nb5")

    assert presenter.format_diff_output(WHITE) == "♝♞♙♙+8"
    assert presenter.format_diff_output(BLACK) == "♚"

    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "no")
    assert presenter.format_diff_output(WHITE) == "BNPP+8"
    assert presenter.format_diff_output(BLACK) == "K"

    # Test unicode padding
    game_config.set_value(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "yes")
    game_config.set_value(game_config.Keys.PAD_UNICODE, "yes")
    assert presenter.format_diff_output(WHITE) == "♝ ♞ ♙ ♙ +8"
    assert presenter.format_diff_output(BLACK) == "♚ "
