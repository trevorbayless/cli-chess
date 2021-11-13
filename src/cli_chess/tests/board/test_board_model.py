import unittest

from chess import Board
from cli_chess.board.board_model import BoardModel


class BoardModelTestCase(unittest.TestCase):

    def test_make_move(self):
        model = BoardModel()

        # Valid standard move
        move = model.make_move("Nf3")
        self.assertEqual(model.board.peek(), move)

        # Illegal standard move
        with self.assertRaises(ValueError):
            move = model.make_move("Qe6")


    def test_set_board_orientation(self):
        model = BoardModel()
        self.assertEqual(model.get_board_orientation(), "white")

        model.set_board_orientation("black")
        self.assertEqual(model.get_board_orientation(), "black")


    def test_get_board_orientation(self):
        model = BoardModel("black")
        self.assertEqual(model.get_board_orientation(), "black")

        model = BoardModel("white")
        self.assertEqual(model.get_board_orientation(), "white")

        model.set_board_orientation("black")
        self.assertEqual(model.get_board_orientation(), "black")


    def test_get_board_squares(self):
        pass


    def test_get_square_file(self):
        pass


    def test_get_square_rank(self):
        pass


    def test_get_file_labels(self):
        pass


    def test_get_rank_label(self):
        pass


    def test_is_square_in_check(self):
        in_check_fen = "8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61"
        model = BoardModel(fen=in_check_fen)
        self.assertTrue(model.is_square_in_check(model.board.king(model.board.turn)))

        not_in_check_fen = "8/8/8/3Q4/8/6K1/8/6k1 w - - 21 61"
        model.board.set_fen(not_in_check_fen)
        self.assertFalse(model.is_square_in_check(model.board.king(model.board.turn)))


    def test_is_white_orientation(self):
        pass
