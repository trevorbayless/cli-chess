import unittest
from cli_chess.board.board_model import BoardModel, Move
from cli_chess.board.board_presenter import BoardPresenter


class BoardPresenterTestCase(unittest.TestCase):
    def test_get_view(self):
        pass


    def test_make_move(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        # Valid move
        move = presenter.make_move("e4")
        self.assertEqual(model.board.peek(), move)

        # Illegal move
        with self.assertRaises(ValueError):
            move = presenter.make_move("O-O-O")


    def test_update_board(self):
        pass


    def test_get_file_labels(self):
        pass


    def test_apply_rank_label(self):
        pass


    def test_get_square_final_display(self):
        pass


    def test_start_new_line(self):
        pass


    def test_get_piece_color(self):
        pass


    def test_get_square_display_color(self):
        pass


    def test_game_result(self):
        pass
