# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.modules.board import BoardModel
import chess
from chess import variant
from unittest.mock import Mock
import pytest


@pytest.fixture
def board_updated_listener():
    return Mock()


@pytest.fixture
def successful_move_listener():
    return Mock()


@pytest.fixture()
def model(board_updated_listener: Mock, successful_move_listener: Mock):
    model = BoardModel()
    model.e_board_model_updated.add_listener(board_updated_listener)
    model.e_successful_move_made.add_listener(successful_move_listener)
    return model


def test_initialize_board():
    # Test standard chess
    model = BoardModel()
    assert type(model.board) == chess.Board
    assert model.get_board_orientation() == chess.WHITE
    assert model.board.fen() == chess.STARTING_FEN

    # Test "startpos" as starting fen
    model = BoardModel(variant="racingKings", fen="startpos")
    assert model.board.fen() == model.board.starting_fen

    # Test chess960 initialization
    model = BoardModel(orientation=chess.BLACK, variant="chess960")
    assert model.board.chess960
    assert type(model.board) == chess.Board
    assert model.get_board_orientation() == chess.BLACK

    # Test a valid variant
    model = BoardModel(variant="crazyhouse", fen="r1b3Bk/p1p4P/2p2p2/3p1p2/3P4/5N2/PPP2PPP/R1BQK2R/QRnbpnpn w KQ - 0 21")
    assert type(model.board) == chess.variant.CrazyhouseBoard
    assert model.board.fen() != model.board.starting_fen
    assert model.get_turn() == chess.WHITE

    # Test an invalid variant
    with pytest.raises(ValueError):
        BoardModel(variant="shogi")


def test_reinitialize_board(model: BoardModel, board_updated_listener: Mock):
    assert model.board.uci_variant == "chess"
    board_updated_listener.assert_not_called()

    # Test invalid initialization
    with pytest.raises(ValueError):
        model.reinitialize_board("checkers")

    assert model.board.uci_variant == "chess"
    board_updated_listener.assert_not_called()

    # Test valid initialization
    model.reinitialize_board("Crazyhouse")
    assert model.board.uci_variant == "crazyhouse"
    board_updated_listener.assert_called()


def test_make_move(model: BoardModel, board_updated_listener: Mock, successful_move_listener: Mock):
    # Test valid move
    try:
        model.make_move("Nf3")
        board_updated_listener.assert_called()
        successful_move_listener.assert_called()
    except Exception as e:
        pytest.fail(f"test_make_move raised {e}")

    # Test illegal move
    # Todo: Test custom exceptions once python-chess updates (IllegalMove, AmbiguousMove, etc)
    board_updated_listener.reset_mock()
    successful_move_listener.reset_mock()
    with pytest.raises(ValueError):
        model.make_move("Qe6")

    board_updated_listener.assert_not_called()
    successful_move_listener.assert_not_called()


def test_takeback(model: BoardModel, board_updated_listener: Mock, successful_move_listener: Mock):
    model.make_move("e4")
    assert model.get_turn() == chess.BLACK
    assert len(model.get_move_stack()) == 1

    # Test a valid takeback
    model.takeback()
    assert len(model.get_move_stack()) == 0
    assert model.get_turn() == chess.WHITE
    board_updated_listener.assert_called()
    successful_move_listener.assert_called()

    # Test empty move stack
    board_updated_listener.reset_mock()
    successful_move_listener.reset_mock()
    model.board.reset()
    with pytest.raises(IndexError):
        model.takeback()

    assert model.get_turn() == chess.WHITE
    board_updated_listener.assert_not_called()
    successful_move_listener.assert_not_called()


def test_get_move_stack(model: BoardModel):
    moves = ["e4", "d6", "d4", "Nf6", "Nc3", "g6"]
    for move in moves:
        model.make_move(move)

    with pytest.raises(ValueError):
        model.make_move("Nb3")

    assert model.get_move_stack() == model.board.move_stack

    # Take back the last move
    model.takeback()
    assert model.get_move_stack() == model.board.move_stack


def test_get_variant_name():
    # Test chess960
    model = BoardModel(variant="chess960")
    assert model.get_variant_name() == "chess960"

    # Test horde
    model = BoardModel(variant="horde")
    assert model.get_variant_name() == "horde"

    # Test racing kings
    model = BoardModel(variant="racingkings")
    assert model.get_variant_name() == "racingkings"

    # Test standard
    model = BoardModel()
    assert model.get_variant_name() == model.board.uci_variant


def test_get_turn():
    # Test model initialized with black board orientation
    model = BoardModel(chess.BLACK)
    assert model.get_turn() == chess.WHITE

    # Test making an invalid move doesn't change the turn
    with pytest.raises(ValueError):
        model.make_move("Ke2")
        assert model.get_turn() == chess.WHITE

    # Test a valid move changes turns
    model.make_move("e4")
    assert model.get_turn() == chess.BLACK

    # Test board initialization with black to play FEN
    model = BoardModel(fen="r1bq1rk1/2p1bppp/p1n2n2/1p1pp3/4P3/1BP2N2/PP1P1PPP/RNBQR1K1 b - - 0 9")
    assert model.get_turn() == chess.BLACK

    # Test taking back a move
    model.make_move("d4")
    model.takeback()
    assert model.get_turn() == chess.BLACK


def test_get_board_orientation():
    model = BoardModel(orientation=chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK

    model = BoardModel()
    assert model.get_board_orientation() == chess.WHITE

    model.set_board_orientation(chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK


def test_set_board_orientation(model: BoardModel, board_updated_listener: Mock):
    assert model.get_board_orientation() == chess.WHITE

    model.set_board_orientation(chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK

    # Test update handler is called on board orientation change
    model.set_board_orientation(chess.BLACK)
    board_updated_listener.assert_called()


def test_set_fen(model: BoardModel, board_updated_listener: Mock):
    model.set_fen("8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 w - - 0 1")
    assert model.board.fen() == "8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 w - - 0 1"
    board_updated_listener.assert_called()

    # Test invalid FENs
    board_updated_listener.reset_mock()
    with pytest.raises(ValueError):
        model.set_fen("")

    with pytest.raises(ValueError):
        model.set_fen("8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 - 0 1")
    board_updated_listener.assert_not_called()


def test_get_board_squares(model: BoardModel):
    square_numbers = [56, 57, 58, 59, 60, 61, 62, 63,
                      48, 49, 50, 51, 52, 53, 54, 55,
                      40, 41, 42, 43, 44, 45, 46, 47,
                      32, 33, 34, 35, 36, 37, 38, 39,
                      24, 25, 26, 27, 28, 29, 30, 31,
                      16, 17, 18, 19, 20, 21, 22, 23,
                      8, 9, 10, 11, 12, 13, 14, 15,
                      0, 1, 2, 3, 4, 5, 6, 7]

    # Test white board orientation
    assert model.get_board_squares() == square_numbers

    # Test black board orientation
    model.set_board_orientation(chess.BLACK)
    assert model.get_board_squares() == square_numbers[::-1]


def test_get_square_file_index(model: BoardModel):
    for square in chess.SQUARES:
        assert model.get_square_file_index(square) == chess.square_file(square)


def test_get_file_labels():
    model = BoardModel()
    file_labels = model.get_file_labels()
    assert file_labels == "a b c d e f g h "

    model.set_board_orientation(chess.BLACK)
    file_labels = model.get_file_labels()
    assert file_labels == "h g f e d c b a "


def test_get_square_rank_index(model: BoardModel):
    for square in chess.SQUARES:
        assert model.get_square_rank_index(square) == chess.square_rank(square)


def test_get_rank_label(model: BoardModel):
    for square in chess.SQUARES:
        rank = chess.square_rank(square)
        assert model.get_rank_label(rank) == chess.RANK_NAMES[rank]


def test_is_square_in_check():
    in_check_fen = "8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61"
    model = BoardModel(fen=in_check_fen)
    assert model.is_square_in_check(model.board.king(model.board.turn))

    not_in_check_fen = "8/8/8/3Q4/8/6K1/8/6k1 w - - 21 61"
    model.set_fen(not_in_check_fen)
    assert not model.is_square_in_check(model.board.king(model.board.turn))


def test_is_light_square():
    model = BoardModel()
    assert not model.is_light_square(chess.H8)
    assert model.is_light_square(chess.A2)
    with pytest.raises(ValueError):
        model.is_light_square(100)


def test_is_white_orientation():
    model = BoardModel()
    assert model.is_white_orientation()
    model.set_board_orientation(chess.BLACK)
    assert not model.is_white_orientation()

    model = BoardModel(orientation=chess.BLACK)
    assert not model.is_white_orientation()
    model.set_board_orientation(chess.WHITE)
    assert model.is_white_orientation()


def test_notify_board_model_updated(model: BoardModel, board_updated_listener: Mock):
    # Test registered board update listener is called
    model._notify_board_model_updated()
    board_updated_listener.assert_called()

    # Unregister listener and test it's not called
    board_updated_listener.reset_mock()
    model.e_board_model_updated.remove_listener(board_updated_listener)
    model._notify_board_model_updated()
    board_updated_listener.assert_not_called()


def test_notify_successful_move_made(model: BoardModel, successful_move_listener: Mock):
    # Test registered successful move listener is called
    model._notify_successful_move_made()
    successful_move_listener.assert_called()

    # Unregister listener and test it's not called
    successful_move_listener.reset_mock()
    model.e_successful_move_made.remove_listener(successful_move_listener)
    model._notify_successful_move_made()
    successful_move_listener.assert_not_called()
