import unittest
import chess
from cli_chess.game.board import BoardModel, BoardPresenter
from cli_chess import config

board_keys = config.BoardKeys

class BoardPresenterTestCase(unittest.TestCase):
    def test_get_view(self):
        model = BoardModel()
        presenter = BoardPresenter(model)
        self.assertEqual(presenter.board_view, presenter.get_view())


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
        model = BoardModel()
        presenter = BoardPresenter(model)

        white_orientation_newline_squares = [chess.H1, chess.H2, chess.H3, chess.H4,
                                             chess.H5, chess.H6, chess.H7, chess.H8]
        black_orientation_newline_squares = [chess.A1, chess.A2, chess.A3, chess.A4,
                                             chess.A5, chess.A6, chess.A7, chess.A8]

        for square in range(chess.A1, len(chess.SQUARES)):
            # Test white orientation newline
            model.set_board_orientation("white")
            output = presenter.start_new_line(square)

            if square in white_orientation_newline_squares:
                self.assertEqual(output, "\n")
            else:
                self.assertEqual(output, "")

            # Test black orientation newline
            model.set_board_orientation("black")
            output = presenter.start_new_line(square)

            if square in black_orientation_newline_squares:
                self.assertEqual(output, "\n")
            else:
                self.assertEqual(output, "")


    def test_get_piece_color(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        defined_light_piece_color = config.get_board_value(board_keys.LIGHT_PIECE_COLOR)
        defined_dark_piece_color = config.get_board_value(board_keys.DARK_PIECE_COLOR)

        # Test light pieces
        for square in range(chess.A1, chess.H2):
            piece = model.board.piece_at(square)
            self.assertEqual(defined_light_piece_color, presenter.get_piece_color(piece))


        # Test dark pieces
        for square in range(chess.A7, chess.H8):
            piece = model.board.piece_at(square)
            self.assertEqual(defined_dark_piece_color, presenter.get_piece_color(piece))


        # Test empty squares
        for square in range(chess.A3, chess.H6):
            piece = model.board.piece_at(square)
            self.assertEqual("", presenter.get_piece_color(piece))


    def test_get_square_display_color(self):
        pass


    def test_game_result(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        white_checkmate_fen = "7k/7R/5N2/3K4/8/8/8/8 b - - 0 1"
        black_checkmate_fen = "8/8/8/8/8/7k/6q1/7K w - - 0 1"
        stalemate_fen = "7k/5K2/6Q1/8/8/8/8/8 b - - 0 1"
        draw_fen = "8/8/8/3k4/8/3K4/8/8 w - - 0 1"
        ongoing_game_fen = "8/3k4/3B1K2/4P3/1Pb5/8/8/8 b - - 0 1"

        # Test white checkmate result
        model.board.set_fen(white_checkmate_fen)
        result = presenter.game_result()
        self.assertEqual(result, "Checkmate - White is victorious")

        # Test black checkmate result
        model.board.set_fen(black_checkmate_fen)
        result = presenter.game_result()
        self.assertEqual(result, "Checkmate - Black is victorious")

        # Test stalemate result
        model.board.set_fen(stalemate_fen)
        result = presenter.game_result()
        self.assertEqual(result, "Stalemate")

        # Test draw result
        model.board.set_fen(draw_fen)
        result = presenter.game_result()
        self.assertEqual(result, "Draw")

        # Test claim draw result
        model.board.set_fen(ongoing_game_fen)
        model.board.result(claim_draw=True)
        result = presenter.game_result()
        self.assertEqual(result, "Draw")
