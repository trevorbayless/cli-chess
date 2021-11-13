import unittest
import chess
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
        self.assertEqual(model.get_board_squares(), square_numbers)

        # Test black board orientation
        model.set_board_orientation("black")
        self.assertEqual(model.get_board_squares(), square_numbers[::-1])


    def test_get_square_file_index(self):
        model = BoardModel()
        file_index = model.get_square_file_index(chess.E4)
        self.assertEqual(file_index, 4)

        file_index = model.get_square_file_index(chess.G6)
        self.assertEqual(file_index, 6)


    def test_get_file_labels(self):
        model = BoardModel()
        file_labels = model.get_file_labels()
        self.assertEqual(file_labels, "a b c d e f g h ")

        model.set_board_orientation("black")
        file_labels = model.get_file_labels()
        self.assertEqual(file_labels, "h g f e d c b a ")


    def test_get_square_rank_index(self):
        model = BoardModel()
        rank_index = model.get_square_rank_index(chess.E4)
        self.assertEqual(rank_index, 3)

        rank_index = model.get_square_rank_index(chess.G6)
        self.assertEqual(rank_index, 5)


    def test_get_rank_label(self):
        model = BoardModel()
        rank_index = model.get_square_rank_index(chess.A1)
        rank_label = model.get_rank_label(rank_index)
        self.assertEqual(rank_label, "1")

        rank_index = model.get_square_rank_index(chess.H8)
        rank_label = model.get_rank_label(rank_index)
        self.assertEqual(rank_label, "8")


    def test_is_square_in_check(self):
        in_check_fen = "8/8/8/8/6K1/8/8/4Q1k1 b - - 21 61"
        model = BoardModel(fen=in_check_fen)
        self.assertTrue(model.is_square_in_check(model.board.king(model.board.turn)))

        not_in_check_fen = "8/8/8/3Q4/8/6K1/8/6k1 w - - 21 61"
        model.board.set_fen(not_in_check_fen)
        self.assertFalse(model.is_square_in_check(model.board.king(model.board.turn)))


    def test_is_white_orientation(self):
        model = BoardModel()
        self.assertTrue(model.is_white_orientation())
        model.set_board_orientation("black")
        self.assertFalse(model.is_white_orientation())

        model = BoardModel("black")
        self.assertFalse(model.is_white_orientation())
        model.set_board_orientation("white")
        self.assertTrue(model.is_white_orientation())
