from cli_chess.modules.material_difference.material_difference_model import MaterialDifferenceModel, PIECE_VALUE
from cli_chess.modules.board import BoardModel
from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
from unittest.mock import Mock
import pytest


@pytest.fixture
def model_listener():
    return Mock()


@pytest.fixture
def model(model_listener: Mock):
    model = MaterialDifferenceModel(BoardModel(fen="7r/8/4k3/8/2P5/2K5/8/3RR3 b - - 0 1"))
    model.e_material_difference_model_updated.add_listener(model_listener)
    return model


def test_default_material_difference(model: MaterialDifferenceModel):
    existing_material_difference = model.material_difference
    default_difference = {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.default_material_difference() == default_difference
    assert model.material_difference == existing_material_difference  # Ensure existing difference wasn't changed


def test_default_score(model: MaterialDifferenceModel):
    existing_score = model.score
    default_score = {WHITE: 0, BLACK: 0}
    assert model.default_score() == default_score
    assert model.score == existing_score  # Ensure score wasn't changed


def test_generate_pieces_fen(model: MaterialDifferenceModel):
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "rkPKRR"
    model.board_model.set_fen("8/3P1k2/3K4/8/8/8/8/8 w - - 0 1")
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "PkK"
    model.board_model.make_move("d8=Q")
    assert model.generate_pieces_fen(model.board_model.board.board_fen()) == "QkK"


def test_reset_all(model: MaterialDifferenceModel):
    assert model.material_difference != model.default_material_difference()
    assert model.score != model.default_score()
    model._reset_all()
    assert model.material_difference == model.default_material_difference()
    assert model.score == model.default_score()


def test_update(model: MaterialDifferenceModel, model_listener: Mock):
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 1, BISHOP: 0, KNIGHT: 0, PAWN: 1},
        BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 6, BLACK: 0}

    # Verify listener was called on material difference model update
    model.update()
    model_listener.assert_called()

    # Verify material difference update method is listening to general board_model update events
    assert model.update in model.board_model.e_board_model_updated.listeners
    model.board_model.set_fen("2q5/8/3q4/2Bk4/1P3Pb1/4K3/8/8 w - - 0 1")
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 2},
        BLACK: {KING: 0, QUEEN: 2, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 0, BLACK: 16}

    model.board_model.make_move("Bxd6")
    assert model.material_difference == {
        WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 2},
        BLACK: {KING: 0, QUEEN: 1, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
    }
    assert model.score == {WHITE: 0, BLACK: 7}

    # Test material difference with horde board
    model = MaterialDifferenceModel(BoardModel(variant="horde"))
    assert model.material_difference == model.default_material_difference()
    assert model.score == model.default_score()

    # Test material difference with 3check board
    model = MaterialDifferenceModel(BoardModel(fen="1B4n1/4k1p1/8/3Bq1p1/p7/P2KN1Pb/3n2pP/8 b - - 0 1", variant="3check"))
    model.board_model.make_moves_from_list(["Qf5", "Nf5", "Bf5"])
    assert model.material_difference == {
        WHITE: {KING: 1, QUEEN: 0, ROOK: 0, BISHOP: 1, KNIGHT: 0, PAWN: 0},
        BLACK: {KING: 2, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 2, PAWN: 1}
    }


def test_update_material_difference(model: MaterialDifferenceModel):
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


def test_update_score(model: MaterialDifferenceModel):
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


def test_get_material_difference(model: MaterialDifferenceModel):
    assert model.get_material_difference(WHITE) == {KING: 0, QUEEN: 0, ROOK: 1, BISHOP: 0, KNIGHT: 0, PAWN: 1}
    assert model.get_material_difference(BLACK) == {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}


def test_get_score(model: MaterialDifferenceModel):
    assert model.score == {WHITE: 6, BLACK: 0}
    assert model.get_score(WHITE) == 6
    assert model.get_score(BLACK) == 0

    model.score = {WHITE: 5, BLACK: 2}
    assert model.get_score(WHITE) == 5
    assert model.get_score(BLACK) == 2


def test_notify_material_difference_model_updated(model: MaterialDifferenceModel, model_listener: Mock):
    # Test registered successful move listener is called
    model._notify_material_difference_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_material_difference_model_updated.remove_listener(model_listener)
    model._notify_material_difference_model_updated()
    model_listener.assert_not_called()
