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

from cli_chess.modules.material_difference.material_difference_model import MaterialDifferenceModel, PIECE_VALUE
from cli_chess.modules.board import BoardModel
from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
from unittest.mock import Mock
import pytest


@pytest.fixture
def model_listener():
    return Mock()


@pytest.fixture
def model(model_listener):
    model = MaterialDifferenceModel(BoardModel(fen="7r/8/4k3/8/2P5/2K5/8/3RR3 b - - 0 1"))
    model.e_material_difference_model_updated.add_listener(model_listener)
    return model


def test_default_material_difference(model):
    existing_material_difference = model.material_difference
    default_difference = {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.default_material_difference() == default_difference
    assert model.material_difference == existing_material_difference  # Ensure existing difference wasn't changed


def test_default_score(model):
    existing_score = model.score
    default_score = {WHITE: 0, BLACK: 0}
    assert model.default_score() == default_score
    assert model.score == existing_score  # Ensure score wasn't changed


def test_generate_pieces_fen(model):
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "rkPKRR"
    model.board_model.set_fen("8/3P1k2/3K4/8/8/8/8/8 w - - 0 1")
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "PkK"
    model.board_model.make_move("d8=Q")
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "QkK"


def test_reset_all(model):
    assert model.material_difference != model.default_material_difference()
    assert model.score != model.default_score()
    model._reset_all()
    assert model.material_difference == model.default_material_difference()
    assert model.score == model.default_score()


def test_update(model, model_listener):
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 1, BISHOP: 0, KNIGHT: 0, PAWN: 1},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 6, BLACK: 0}

    # Verify listener was called on material difference model update
    model.update()
    model_listener.assert_called()

    # Verify material difference update method is listening to general board_model update events
    model.board_model.set_fen("2q5/8/3q4/2Bk4/1P3Pb1/4K3/8/8 w - - 0 1")
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 2},
        BLACK: {KING: 0, QUEEN: 2, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 0, BLACK: 16}

    # Verify material difference update method is listening to successful move board_model update events
    model.board_model.make_move("Bxd6")
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 2},
        BLACK: {KING: 0, QUEEN: 1, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 0, BLACK: 7}


def test_update_material_difference(model):
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 1, BISHOP: 0, KNIGHT: 0, PAWN: 1},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }

    model._update_material_difference(BLACK, ROOK)
    model._update_material_difference(WHITE, QUEEN)
    model._update_material_difference(BLACK, PAWN)

    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 1, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }


def test_update_score(model):
    # Verify piece values are correct
    assert PIECE_VALUE == {
        KING: 0,
        QUEEN: 9,
        ROOK: 5,
        BISHOP: 3,
        KNIGHT: 3,
        PAWN: 1,
    }

    # Verify score updates correctly
    assert model.score == {WHITE: 6, BLACK: 0}
    model._update_score(BLACK, QUEEN)
    assert model.get_score(BLACK) == 3
    assert model.score == {WHITE: 0, BLACK: 3}
    model._update_score(WHITE, KNIGHT)
    assert model.get_score(WHITE) == 0
    assert model.score == {WHITE: 0, BLACK: 0}


def test_get_material_difference(model):
    assert model.get_material_difference(WHITE) == {KING: 0, QUEEN: 0, ROOK: 1, BISHOP: 0, KNIGHT: 0, PAWN: 1}
    assert model.get_material_difference(BLACK) == {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}


def test_get_score(model):
    assert model.score == {WHITE: 6, BLACK: 0}
    assert model.get_score(WHITE) == 6
    assert model.get_score(BLACK) == 0

    model.score = {WHITE: 5, BLACK: 2}
    assert model.get_score(WHITE) == 5
    assert model.get_score(BLACK) == 2


def test_notify_material_difference_model_updated(model, model_listener):
    # Test registered successful move listener is called
    model._notify_material_difference_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_material_difference_model_updated.remove_listener(model_listener)
    model._notify_material_difference_model_updated()
    model_listener.assert_not_called()
