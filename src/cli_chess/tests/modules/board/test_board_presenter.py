# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.modules.board import BoardModel, BoardPresenter
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import BoardSection
from os import remove
import chess
import pytest


@pytest.fixture
def model():
    return BoardModel()


@pytest.fixture
def board_config():
    board_config = BoardSection("unit_test_config.ini")
    yield board_config
    remove(board_config.full_filename)


@pytest.fixture
def presenter(model, board_config, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.board.board_presenter.board_config', board_config)
    return BoardPresenter(model)


def test_update(model, presenter, board_config):
    # Todo: Still trying to determine best way to test.
    #       see comment in board_presenter.py for options
    pass


def test_update_cached_config_values(model, presenter, board_config):
    # Test initial assignment
    assert presenter.board_config_values == board_config.get_all_values()
    assert not presenter.board_config_values[board_config.Keys.BLINDFOLD_CHESS.value["name"]]
    assert presenter.board_config_values[board_config.Keys.USE_UNICODE_PIECES.value["name"]]

    # Test board_config listener notification is working
    # (manual calls to _update_cached_config_values shouldn't be required)
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "yes")
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.board_config_values == board_config.get_all_values()
    assert presenter.board_config_values[board_config.Keys.BLINDFOLD_CHESS.value["name"]]
    assert not presenter.board_config_values[board_config.Keys.USE_UNICODE_PIECES.value["name"]]

    # Remove board config notification listener and verify updates don't come through
    board_config.e_board_config_updated.remove_listener(presenter._update_cached_config_values)
    assert presenter.board_config_values == board_config.get_all_values()
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    assert presenter.board_config_values != board_config.get_all_values()

    # With listener removed, manually call the function and verify it works by itself
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "no")
    assert presenter.board_config_values != board_config.get_all_values()
    presenter._update_cached_config_values()
    assert presenter.board_config_values == board_config.get_all_values()


def test_make_move(model, presenter):
    try:
        presenter.make_move("e4")
        assert model.board.board_fen() == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
    except Exception as e:
        pytest.fail(f"test_make_move raised {e}")

    # Todo: Test custom exceptions once python-chess updates (IllegalMove, AmbiguousMove, etc)
    with pytest.raises(ValueError):
        presenter.make_move("O-O-O")


def test_get_board_display(model, presenter, board_config):
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "no")
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "yes")
    board_config.set_value(board_config.Keys.IN_CHECK_COLOR, "purple")
    board_config.set_value(board_config.Keys.LIGHT_SQUARE_COLOR, "teal")
    board_config.set_value(board_config.Keys.DARK_SQUARE_COLOR, "orange")
    board_config.set_value(board_config.Keys.LIGHT_PIECE_COLOR, "white")
    board_config.set_value(board_config.Keys.DARK_PIECE_COLOR, "black")

    model.set_fen("8/P2R2B1/4p3/5ppQ/1q1nP3/1P1P4/3K1kB1/b7 w - - 0 1")  # white in check
    board_output = presenter.get_board_display()

    for square_data in board_output:
        # Test square in check
        if square_data['square_number'] == chess.D2:
            assert square_data == {
                'square_number': chess.D2,
                'piece_str': 'K',
                'piece_display_color': 'white',
                'square_display_color': 'purple',
                'rank_label': '',
                'is_end_of_rank': False
            }

        # Test start of rank with rank label
        if square_data['square_number'] == chess.A1:
            assert square_data == {
                'square_number': chess.A1,
                'piece_str': 'b',
                'piece_display_color': 'black',
                'square_display_color': 'orange',
                'rank_label': '1',
                'is_end_of_rank': False
            }

        # Test end of rank without piece
        if square_data['square_number'] == chess.H7:
            assert square_data == {
                'square_number': chess.H7,
                'piece_str': '',
                'piece_display_color': '',
                'square_display_color': 'teal',
                'rank_label': '',
                'is_end_of_rank': True
            }


def test_get_file_labels(model, presenter, board_config):
    board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "yes")
    assert presenter.get_file_labels() == model.get_file_labels()

    board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "no")
    assert presenter.get_file_labels() == ""


def test_get_file_label_color(model, presenter, board_config):
    board_config.set_value(board_config.Keys.FILE_LABEL_COLOR, "yellow")
    assert presenter.get_file_label_color() == "yellow"


def test_get_rank_label_color(model, presenter, board_config):
    board_config.set_value(board_config.Keys.RANK_LABEL_COLOR, "purple")
    assert presenter.get_rank_label_color() == "purple"


def test_get_rank_label(model, presenter, board_config):
    # Test white orientation with board coordinates
    board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "yes")
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
    board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "no")
    for square in chess.SQUARES:
        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            assert presenter.get_rank_label(square) == ""
        else:
            assert presenter.get_rank_label(square) == ""


def test_is_square_start_of_rank(model, presenter, board_config):
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


def test_is_square_end_of_rank(model, presenter, board_config):
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


def test_get_piece_str(model, presenter, board_config):
    # Test unicode pieces
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "no")
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        if piece:
            assert presenter.get_piece_str(square) == get_piece_unicode_symbol(piece.symbol())
        else:
            assert presenter.get_piece_str(square) == ""

    # Test letter pieces
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        if piece:
            assert presenter.get_piece_str(square) == piece.symbol()
        else:
            assert presenter.get_piece_str(square) == ""

    # Test blindfold chess
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "yes")
    for square in chess.SQUARES:
        assert presenter.get_piece_str(square) == ""


def test_get_piece_display_color(model, presenter, board_config):
    board_config.set_value(board_config.Keys.LIGHT_PIECE_COLOR, "gray")
    board_config.set_value(board_config.Keys.DARK_PIECE_COLOR, "navy")

    for square in chess.SQUARES:
        piece = model.board.piece_at(square)
        bb = chess.BB_SQUARES[square]

        # Test light piece color
        if bb & chess.BB_RANK_1 or bb & chess.BB_RANK_2:
            assert presenter.get_piece_display_color(piece) == "gray"

        # Test dark piece color
        elif bb & chess.BB_RANK_7 or bb & chess.BB_RANK_8:
            assert presenter.get_piece_display_color(piece) == "navy"

        # Test no piece
        else:
            assert presenter.get_piece_display_color(piece) == ""


def test_get_square_display_color(model, presenter, board_config):
    board_config.set_value(board_config.Keys.LIGHT_SQUARE_COLOR, "white")
    board_config.set_value(board_config.Keys.DARK_SQUARE_COLOR, "blue")
    board_config.set_value(board_config.Keys.SHOW_BOARD_HIGHLIGHTS, "yes")
    board_config.set_value(board_config.Keys.LAST_MOVE_COLOR, "yellow")
    board_config.set_value(board_config.Keys.IN_CHECK_COLOR, "red")

    model.set_fen("rnbqkbnr/ppppp1pp/8/5p2/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
    presenter.make_move("Qh5")  # black in check
    last_move = model.board.peek()

    for square in chess.SQUARES:
        # Test in check square
        if model.is_square_in_check(square):
            assert presenter.get_square_display_color(square) == "red"

        # Test last move squares
        elif square == last_move.to_square or square == last_move.from_square:
            assert presenter.get_square_display_color(square) == "yellow"

        # Test light square
        elif model.is_light_square(square):
            assert presenter.get_square_display_color(square) == "white"

        # Test dark square
        elif not model.is_light_square(square):
            assert presenter.get_square_display_color(square) == "blue"

    # Test board highlights disabled (no last move color)
    board_config.set_value(board_config.Keys.SHOW_BOARD_HIGHLIGHTS, "no")
    presenter.make_move("g6")
    last_move = model.board.peek()

    if chess.BB_SQUARES[last_move.to_square] & chess.BB_LIGHT_SQUARES:
        assert presenter.get_square_display_color(last_move.to_square) == "white"

    if chess.BB_SQUARES[last_move.from_square] & chess.BB_DARK_SQUARES:
        assert presenter.get_square_display_color(last_move.from_square) == "blue"


def test_game_result(model, presenter):
    white_checkmate_fen = "7k/7R/5N2/3K4/8/8/8/8 b - - 0 1"
    black_checkmate_fen = "8/8/8/8/8/7k/6q1/7K w - - 0 1"
    stalemate_fen = "7k/5K2/6Q1/8/8/8/8/8 b - - 0 1"
    draw_fen = "8/8/8/3k4/8/3K4/8/8 w - - 0 1"
    ongoing_game_fen = "8/3k4/3B1K2/4P3/1Pb5/8/8/8 b - - 0 1"

    # Test white checkmate result
    model.set_fen(white_checkmate_fen)
    result = presenter.game_result()
    assert result == "Checkmate - White is victorious"

    # Test black checkmate result
    model.set_fen(black_checkmate_fen)
    result = presenter.game_result()
    assert result == "Checkmate - Black is victorious"

    # Test stalemate result
    model.set_fen(stalemate_fen)
    result = presenter.game_result()
    assert result == "Stalemate"

    # Test draw result
    model.set_fen(draw_fen)
    result = presenter.game_result()
    assert result == "Draw"

    # Test claim draw result
    model.set_fen(ongoing_game_fen)
    model.board.result(claim_draw=True)
    result = presenter.game_result()
    assert result == "Draw"
