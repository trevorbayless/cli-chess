from cli_chess.modules.board import BoardModel
from unittest.mock import Mock
import pytest
import chess
import chess.variant


@pytest.fixture
def board_updated_listener():
    return Mock()


@pytest.fixture()
def model(board_updated_listener: Mock):
    model = BoardModel()
    model.e_board_model_updated.add_listener(board_updated_listener)
    return model


def test_initialize_board():
    # Test standard chess
    model = BoardModel()
    assert isinstance(model.board, chess.Board)
    assert model.get_board_orientation() == chess.WHITE
    assert model.board.fen() == chess.STARTING_FEN
    assert model.get_highlight_move() == chess.Move.null()

    # Test "startpos" as starting fen
    model = BoardModel(variant="racingKings", fen="startpos")
    assert model.board.fen() == model.board.starting_fen

    # Test initializing an empty board
    model = BoardModel(variant="racingKings", fen=None)
    assert model.board.fen() == "8/8/8/8/8/8/8/8 w - - 0 1"
    assert model.board.occupied == chess.BB_EMPTY

    # Test chess960 initialization
    model = BoardModel(orientation=chess.BLACK, variant="chess960")
    assert model.board.chess960
    assert isinstance(model.board, chess.Board)
    assert model.get_board_orientation() == chess.BLACK

    # Test a valid variant
    model = BoardModel(variant="crazyhouse", fen="r1b3Bk/p1p4P/2p2p2/3p1p2/3P4/5N2/PPP2PPP/R1BQK2R/QRnbpnpn w KQ - 0 21")
    assert isinstance(model.board, chess.variant.CrazyhouseBoard)
    assert model.board.fen() != model.board.starting_fen
    assert model.get_turn() == chess.WHITE

    # Test racing kings starts as white orientation regardless
    model = BoardModel(variant="racingKings", orientation=chess.BLACK)
    assert model.get_board_orientation() == chess.WHITE

    # Test an invalid variant
    with pytest.raises(ValueError):
        BoardModel(variant="shogi")


def test_reinitialize_board(model: BoardModel, board_updated_listener: Mock):
    assert model.board.uci_variant == "chess"
    board_updated_listener.assert_not_called()

    # Test invalid initialization
    with pytest.raises(ValueError):
        model.reinitialize_board("checkers", chess.WHITE)

    assert model.board.uci_variant == "chess"
    board_updated_listener.assert_not_called()

    # Test valid initialization
    model.reinitialize_board("Horde", chess.BLACK, uci_last_move="e2e4")
    assert model.board.uci_variant == "horde"
    assert model.orientation == chess.BLACK
    assert model.initial_fen == model.board.starting_fen
    assert model.get_highlight_move() == chess.Move.from_uci("e2e4")
    board_updated_listener.assert_called()

    # Test racing kings starts as white orientation regardless
    model.reinitialize_board("racingKings", orientation=chess.BLACK)
    assert model.get_board_orientation() == chess.WHITE
    assert model.get_highlight_move() == chess.Move.null()


def test_make_move(model: BoardModel, board_updated_listener: Mock):
    # Test valid move
    try:
        model.make_move("Nf3")
        board_updated_listener.assert_called()
        assert model.get_highlight_move() == model.board.peek()
    except Exception as e:
        pytest.fail(f"test_make_move raised {e}")

    # Test illegal move
    # Todo: Test custom exceptions once python-chess updates (IllegalMove, AmbiguousMove, etc)
    board_updated_listener.reset_mock()
    with pytest.raises(ValueError):
        model.make_move("Qe6")

    board_updated_listener.assert_not_called()
    assert model.get_highlight_move() == model.board.peek()


def test_make_moves_from_list(model: BoardModel, board_updated_listener: Mock):
    # Test a valid move sequence
    moves = ["e4", "g6", "d4", "Bg7"]
    model.make_moves_from_list(moves)
    assert model.board.peek() == chess.Move.from_uci("f8g7")
    assert model.get_highlight_move() == chess.Move.from_uci("f8g7")
    board_updated_listener.assert_called()

    # Test an invalid sequence
    board_updated_listener.reset_mock()
    moves = ["Nf3", "Bh8"]  # Bh8 is invalid
    with pytest.raises(ValueError):
        model.make_moves_from_list(moves)
    assert model.board.peek() == chess.Move.from_uci("g1f3")
    assert model.get_highlight_move() == chess.Move.from_uci("g1f3")
    board_updated_listener.assert_not_called()


def test_takeback(model: BoardModel, board_updated_listener: Mock):
    # Test empty move stack
    model.board.reset()
    with pytest.raises(Warning):
        model.takeback(chess.WHITE)

    assert model.get_turn() == chess.WHITE
    assert model.get_highlight_move() == chess.Move.null()
    board_updated_listener.assert_not_called()

    # Ensure callbacks are called on successful takeback
    model.make_move("e4")
    model.takeback(chess.WHITE)
    assert model.get_turn() == chess.WHITE
    assert len(model.get_move_stack()) == 0
    board_updated_listener.assert_called()

    # Ensure callbacks are not called on unsuccessful takebacks
    model.make_move("e4")
    board_updated_listener.reset_mock()
    with pytest.raises(Warning):
        model.takeback(chess.BLACK)
    board_updated_listener.assert_not_called()

    # Test a valid black takeback
    model.board.reset()
    model.make_moves_from_list(["e4", "e5"])
    model.takeback(chess.BLACK)
    assert len(model.get_move_stack()) == 1
    assert model.get_turn() == chess.BLACK
    assert model.get_highlight_move() == model.board.peek()

    # Test takebacks can occur even if the opponent has moved since
    model.board.reset()
    model.make_moves_from_list(["e4", "e5", "Nf3", "Nf6"])
    model.takeback(chess.WHITE)
    assert len(model.get_move_stack()) == 2
    assert model.get_turn() == chess.WHITE


def test_get_move_stack(model: BoardModel):
    moves = ["e4", "d6", "d4", "Nf6", "Nc3", "g6"]
    model.make_moves_from_list(moves)

    with pytest.raises(ValueError):
        model.make_move("Nb3")

    assert model.get_move_stack() == model.board.move_stack

    # Take back the last move
    model.takeback(chess.WHITE)
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

    # Test without model update notification
    board_updated_listener.reset_mock()
    model.set_board_orientation(chess.WHITE, notify=False)
    board_updated_listener.assert_not_called()


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

    # Test without model update notification
    board_updated_listener.reset_mock()
    model.set_fen("8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 w - - 0 1", notify=False)
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


def test_set_board_position(model: BoardModel, board_updated_listener: Mock):
    # Test with all valid parameters
    model.set_board_position(fen="8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61", uci_last_move="e2e1")
    assert model.board.fen() == "8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61"
    assert model.get_highlight_move() == chess.Move.from_uci("e2e1")

    # Test without orientation and uci_last_move forced highlight
    board_updated_listener.reset_mock()
    model.set_board_position(fen="8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 w - - 0 1")
    assert model.board.fen() == "8/4p3/pP2p2K/1N1qnp2/4k1P1/7P/5PR1/3BB3 w - - 0 1"
    board_updated_listener.assert_called()
    assert model.get_highlight_move() == chess.Move.null()


def test_is_game_over(model: BoardModel):
    # Test game in progress
    model.set_fen("k7/8/8/8/8/8/8/K5Q1 w - - 0 1")
    assert not model.is_game_over()

    # Test game over
    model.make_move("Qb6")  # stalemate
    assert model.is_game_over()


def test_get_game_over_result(model: BoardModel):
    # Test game in progress
    model.set_fen("8/6q1/6k1/8/2K5/8/8/8 w - - 0 1")

    # Test game over with a standard termination reason
    model.set_fen("7K/6q1/6k1/8/8/8/8/8 w - - 0 1")
    assert model.get_game_over_result() == chess.Outcome(chess.Termination.CHECKMATE, chess.BLACK)

    # Test game over by resignation
    model.set_fen("8/8/4K3/8/3pk3/8/8/8 b - - 0 1")
    model.handle_resignation(chess.WHITE)
    assert model.get_game_over_result() == chess.Outcome("resignation", chess.BLACK)  # noqa


def test_handle_resignation(model: BoardModel):
    # Test white resignation
    model.set_fen("8/1PK5/8/8/8/4q3/8/1k6 b - - 0 1")
    model.handle_resignation(chess.WHITE)
    assert model.get_game_over_result() == chess.Outcome("resignation", chess.BLACK)  # noqa
    assert model.is_game_over()

    # Test black resignation
    model.set_fen("8/3k4/3B1K2/4P3/1Pb5/8/8/8 b - - 0 1")
    model.handle_resignation(chess.BLACK)
    assert model.get_game_over_result() == chess.Outcome("resignation", chess.WHITE)  # noqa


def test_cleanup(model: BoardModel, board_updated_listener: Mock):
    assert len(model.e_board_model_updated.listeners) > 0
    model.cleanup()
    assert len(model.e_board_model_updated.listeners) == 0


def test_notify_board_model_updated(model: BoardModel, board_updated_listener: Mock):
    # Test registered board update listener is called
    model._notify_board_model_updated()
    board_updated_listener.assert_called()

    # Unregister listener and test it's not called
    board_updated_listener.reset_mock()
    model.e_board_model_updated.remove_listener(board_updated_listener)
    model._notify_board_model_updated()
    board_updated_listener.assert_not_called()
