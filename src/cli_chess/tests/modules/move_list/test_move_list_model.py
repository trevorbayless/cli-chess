from cli_chess.modules.move_list import MoveListModel
from cli_chess.modules.board import BoardModel
from chess import WHITE, BLACK, PIECE_SYMBOLS, KING, QUEEN, BISHOP, PAWN
from unittest.mock import Mock
import pytest


@pytest.fixture
def model_listener():
    return Mock()


@pytest.fixture()
def model(model_listener: Mock):
    model = MoveListModel(BoardModel())
    model.e_move_list_model_updated.add_listener(model_listener)
    return model


def test_update(model: MoveListModel, model_listener: Mock):
    # Verify this method is listening to board model updates
    assert model.update in model.board_model.e_board_model_updated.listeners

    model.board_model.set_fen("2bqkbnr/P2ppppp/8/8/8/8/1PPPPPPP/RNBQK2R w KQk - 0 1")
    assert len(model.move_list_data) == 0

    # Test castling
    model.board_model.make_move("O-O")
    move_data = {
        'turn': WHITE,
        'move': 'O-O',
        'piece_type': KING,
        'piece_symbol': PIECE_SYMBOLS[KING],
        'is_castling': True,
        'is_promotion': False
    }
    assert model.move_list_data == [move_data]

    # Test invalid move
    with pytest.raises(ValueError):
        model.board_model.make_move("Ke7")
    assert model.move_list_data == [move_data]

    # Test black turn
    model.board_model.make_move("c8b7")
    assert model.move_list_data[-1] == {
        'turn': BLACK,
        'move': 'Bb7',
        'piece_type': BISHOP,
        'piece_symbol': PIECE_SYMBOLS[BISHOP],
        'is_castling': False,
        'is_promotion': False
    }

    # Test promotion
    model.board_model.make_move("a8Q")
    assert model.move_list_data[-1] == {
        'turn': WHITE,
        'move': 'a8=Q',
        'piece_type': PAWN,
        'piece_symbol': PIECE_SYMBOLS[PAWN],
        'is_castling': False,
        'is_promotion': True
    }

    # Test a null move
    model.board_model.make_move("0000")
    assert model.move_list_data[-1] == {
        'turn': BLACK,
        'move': '--',
        'piece_type': None,
        'piece_symbol': None,
        'is_castling': False,
        'is_promotion': False
    }

    # Test crazyhouse drop piece
    model = MoveListModel(BoardModel(variant="crazyhouse", fen="kr6/1Q6/8/8/8/8/8/K7 b - - 0 1"))
    model.board_model.make_move("Rb7")
    model.board_model.make_move("Ka2")
    model.board_model.make_move("Q@a7")
    assert model.move_list_data[-1] == {
        'turn': BLACK,
        'move': 'Q@a7#',
        'piece_type': QUEEN,
        'piece_symbol': PIECE_SYMBOLS[QUEEN],
        'is_castling': False,
        'is_promotion': False
    }

    # Verify the move list model update notification is sent to listeners
    model_listener.assert_called()


def test_get_move_list_data(model: MoveListModel):
    assert len(model.get_move_list_data()) == 0
    model.board_model.set_fen("1n6/NpP5/1P1PP1b1/k2pR3/2pK4/6r1/1p3P2/8 b - - 0 1")
    model.board_model.make_move("Be4")
    assert model.get_move_list_data() == [{
        'turn': BLACK,
        'move': 'Be4',
        'piece_type': BISHOP,
        'piece_symbol': 'b',
        'is_castling': False,
        'is_promotion': False
    }]
    assert model.get_move_list_data() == model.move_list_data
    model.board_model.takeback(BLACK)
    assert model.get_move_list_data() == []


def test_notify_move_list_model_updated(model: MoveListModel, model_listener: Mock):
    # Test registered successful move listener is called
    model._notify_move_list_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_move_list_model_updated.remove_listener(model_listener)
    model._notify_move_list_model_updated()
    model_listener.assert_not_called()
