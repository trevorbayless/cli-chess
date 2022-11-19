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

import pytest
import chess
from cli_chess.modules.board import BoardModel


def test_make_move():
    model = BoardModel()

    # Test valid move
    try:
        model.make_move("Nf3")
    except Exception as e:
        pytest.fail(f"test_make_move raised {e}")

    # Test illegal move
    with pytest.raises(ValueError):
        model.make_move("Qe6")


def test_get_move_stack():
    pass


def test_get_variant_name():
    pass


def test_random_orientation():
    pass


def test_set_board_orientation():
    model = BoardModel()
    assert model.get_board_orientation() == chess.WHITE

    model.set_board_orientation(chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK


def test_get_board_orientation():
    model = BoardModel(my_color=chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK

    model = BoardModel()
    assert model.get_board_orientation() == chess.WHITE

    model.set_board_orientation(chess.BLACK)
    assert model.get_board_orientation() == chess.BLACK


def test_get_board_squares():
    model = BoardModel()
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


def test_get_square_file_index():
    model = BoardModel()
    file_index = model.get_square_file_index(chess.E4)
    assert file_index == 4

    file_index = model.get_square_file_index(chess.G6)
    assert file_index == 6


def test_get_file_labels():
    model = BoardModel()
    file_labels = model.get_file_labels()
    assert file_labels == "a b c d e f g h "

    model.set_board_orientation(chess.BLACK)
    file_labels = model.get_file_labels()
    assert file_labels == "h g f e d c b a "


def test_get_square_rank_index():
    model = BoardModel()
    rank_index = model.get_square_rank_index(chess.E4)
    assert rank_index == 3

    rank_index = model.get_square_rank_index(chess.G6)
    assert rank_index == 5


def test_get_rank_label():
    model = BoardModel()
    rank_index = model.get_square_rank_index(chess.A1)
    rank_label = model.get_rank_label(rank_index)
    assert rank_label == "1"

    rank_index = model.get_square_rank_index(chess.H8)
    rank_label = model.get_rank_label(rank_index)
    assert rank_label == "8"


def test_is_square_in_check():
    in_check_fen = "8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61"
    model = BoardModel(fen=in_check_fen)
    assert model.is_square_in_check(model.board.king(model.board.turn))

    not_in_check_fen = "8/8/8/3Q4/8/6K1/8/6k1 w - - 21 61"
    model.board.set_fen(not_in_check_fen)
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

    model = BoardModel(my_color=chess.BLACK)
    assert not model.is_white_orientation()
    model.set_board_orientation(chess.WHITE)
    assert model.is_white_orientation()
