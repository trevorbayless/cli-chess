from cli_chess.modules.board import BoardModel, BoardPresenter
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import GameConfig
from os import remove
import chess
from unittest.mock import Mock
import pytest


@pytest.fixture
def model():
    return BoardModel()


@pytest.fixture
def presenter(model: BoardModel, game_config: GameConfig, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.board.board_presenter.game_config', game_config)
    return BoardPresenter(model)


@pytest.fixture
def game_config():
    game_config = GameConfig("unit_test_config.ini")
    yield game_config
    remove(game_config.full_filename)


def test_update(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Verify the update method is listening to model updates
    assert presenter.update in model.e_board_model_updated.listeners

    # Verify the board presenter update function is calling the board view
    # update function and passing in the board output data
    model.make_move("Nf3")
    presenter.view.update = Mock()
    presenter.update()
    board_output_data = presenter.get_board_display()
    presenter.view.update.assert_called_with(board_output_data)


def test_update_cached_config_values(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Verify the method is listening to game configuration updates
    assert presenter._update_cached_config_values in game_config.e_game_config_updated.listeners

    # Test initial assignment
    assert presenter.game_config_values == game_config.get_all_values()

    # Test game_config listener notification is working
    # (manual calls to _update_cached_config_values shouldn't be required)
    game_config.set_value(game_config.Keys.BLINDFOLD_CHESS, "yes")
    game_config.set_value(game_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.game_config_values == game_config.get_all_values()
    assert presenter.game_config_values[game_config.Keys.BLINDFOLD_CHESS]
    assert not presenter.game_config_values[game_config.Keys.USE_UNICODE_PIECES]

    # Remove game config notification listener and verify updates don't come through
    game_config.e_game_config_updated.remove_listener(presenter._update_cached_config_values)
    assert presenter.game_config_values == game_config.get_all_values()
    game_config.set_value(game_config.Keys.USE_UNICODE_PIECES, "yes")
    assert presenter.game_config_values != game_config.get_all_values()

    # With listener removed, manually call the function and verify it works by itself
    game_config.set_value(game_config.Keys.BLINDFOLD_CHESS, "no")
    assert presenter.game_config_values != game_config.get_all_values()
    presenter._update_cached_config_values()
    assert presenter.game_config_values == game_config.get_all_values()


def test_make_move(model: BoardModel, presenter: BoardPresenter):
    try:
        presenter.make_move("e4")
        assert model.board.board_fen() == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
    except Exception as e:
        pytest.fail(f"test_make_move raised {e}")

    # Todo: Test custom exceptions once python-chess updates (IllegalMove, AmbiguousMove, etc)
    with pytest.raises(ValueError):
        presenter.make_move("O-O-O")


def test_get_board_display(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    game_config.set_value(game_config.Keys.BLINDFOLD_CHESS, "no")
    game_config.set_value(game_config.Keys.USE_UNICODE_PIECES, "no")
    game_config.set_value(game_config.Keys.SHOW_BOARD_COORDINATES, "yes")

    model.set_fen("8/P2R2B1/4p3/5ppQ/1q1nP3/1P1P4/3K1kB1/b7 w - - 0 1")  # white in check
    board_output = presenter.get_board_display()

    for square_data in board_output:
        # Test square in check
        if square_data['square_number'] == chess.D2:
            assert square_data == {
                'square_number': chess.D2,
                'piece_str': 'K',
                'piece_display_color': 'light-piece',
                'square_display_color': 'in-check',
                'rank_label': '',
                'is_end_of_rank': False
            }

        # Test start of rank with rank label
        if square_data['square_number'] == chess.A1:
            assert square_data == {
                'square_number': chess.A1,
                'piece_str': 'B',
                'piece_display_color': 'dark-piece',
                'square_display_color': 'dark-square',
                'rank_label': '1',
                'is_end_of_rank': False
            }

        # Test end of rank without piece
        if square_data['square_number'] == chess.H7:
            assert square_data == {
                'square_number': chess.H7,
                'piece_str': '',
                'piece_display_color': '',
                'square_display_color': 'light-square',
                'rank_label': '',
                'is_end_of_rank': True
            }


def test_get_file_labels(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    game_config.set_value(game_config.Keys.SHOW_BOARD_COORDINATES, "yes")
    assert presenter.get_file_labels() == model.get_file_labels()

    game_config.set_value(game_config.Keys.SHOW_BOARD_COORDINATES, "no")
    assert presenter.get_file_labels() == ""


def test_get_rank_label(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Test white orientation with board coordinates
    game_config.set_value(game_config.Keys.SHOW_BOARD_COORDINATES, "yes")
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_A:
            assert presenter.get_rank_label(square) == model.get_rank_label(chess.square_rank(square))
        else:
            assert presenter.get_rank_label(square) == ""

    # Test black orientation with board coordinates
    model.set_board_orientation(chess.BLACK)
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            assert presenter.get_rank_label(square) == model.get_rank_label(chess.square_rank(square))
        else:
            assert presenter.get_rank_label(square) == ""

    # Test with board coordinates disabled
    game_config.set_value(game_config.Keys.SHOW_BOARD_COORDINATES, "no")
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            assert presenter.get_rank_label(square) == ""
        else:
            assert presenter.get_rank_label(square) == ""


def test_is_square_start_of_rank(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Test start of rank white orientation
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_A:
            assert presenter.is_square_start_of_rank(square)
        else:
            assert not presenter.is_square_start_of_rank(square)

    # Test end of rank black orientation
    model.set_board_orientation(chess.BLACK)
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            assert presenter.is_square_start_of_rank(square)
        else:
            assert not presenter.is_square_start_of_rank(square)


def test_is_square_end_of_rank(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Test end of rank white orientation
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            assert presenter.is_square_end_of_rank(square)
        else:
            assert not presenter.is_square_end_of_rank(square)

    # Test end of rank black orientation
    model.set_board_orientation(chess.BLACK)
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_A:
            assert presenter.is_square_end_of_rank(square)
        else:
            assert not presenter.is_square_end_of_rank(square)


def test_get_piece_str(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    # Test unicode pieces
    game_config.set_value(game_config.Keys.BLINDFOLD_CHESS, "no")
    game_config.set_value(game_config.Keys.USE_UNICODE_PIECES, "yes")
    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        if piece:
            assert presenter.get_piece_str(square) == get_piece_unicode_symbol(piece.symbol())
        else:
            assert presenter.get_piece_str(square) == ""

    # Test letter pieces
    game_config.set_value(game_config.Keys.USE_UNICODE_PIECES, "no")
    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        if piece:
            assert presenter.get_piece_str(square) == piece.symbol().upper()
        else:
            assert presenter.get_piece_str(square) == ""

    # Test blindfold chess
    game_config.set_value(game_config.Keys.BLINDFOLD_CHESS, "yes")
    for square in chess.SQUARES:
        assert presenter.get_piece_str(square) == ""


def test_get_piece_display_color(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        bb = chess.BB_SQUARES[square]

        # Test light piece color
        if bb & chess.BB_RANK_1 or bb & chess.BB_RANK_2:
            assert presenter.get_piece_display_color(piece) == "light-piece"

        # Test dark piece color
        elif bb & chess.BB_RANK_7 or bb & chess.BB_RANK_8:
            assert presenter.get_piece_display_color(piece) == "dark-piece"

        # Test no piece
        else:
            assert presenter.get_piece_display_color(piece) == ""


def test_get_square_display_color(model: BoardModel, presenter: BoardPresenter, game_config: GameConfig):
    game_config.set_value(game_config.Keys.SHOW_BOARD_HIGHLIGHTS, "yes")

    model.set_fen("rnbqkbnr/ppppp1pp/8/5p2/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
    presenter.make_move("Qh5")  # black in check
    last_move = model.board.peek()

    for square in chess.SQUARES:
        # Test in check square
        if model.is_square_in_check(square):
            assert presenter.get_square_display_color(square) == "in-check"

        # Test last move squares
        elif square == last_move.to_square or square == last_move.from_square:
            assert presenter.get_square_display_color(square) == "last-move"

        # Test light square
        elif model.is_light_square(square):
            assert presenter.get_square_display_color(square) == "light-square"

        # Test dark square
        elif not model.is_light_square(square):
            assert presenter.get_square_display_color(square) == "dark-square"

    # Test board highlights disabled (no last move color)
    game_config.set_value(game_config.Keys.SHOW_BOARD_HIGHLIGHTS, "no")
    presenter.make_move("g6")
    last_move = model.board.peek()

    if chess.BB_SQUARES[last_move.to_square] & chess.BB_LIGHT_SQUARES:
        assert presenter.get_square_display_color(last_move.to_square) == "light-square"

    if chess.BB_SQUARES[last_move.from_square] & chess.BB_DARK_SQUARES:
        assert presenter.get_square_display_color(last_move.from_square) == "dark-square"
