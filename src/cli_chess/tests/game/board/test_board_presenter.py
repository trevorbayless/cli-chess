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

from cli_chess.game_components.board import BoardModel, BoardPresenter
from cli_chess.game_components.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
import unittest
import chess

class BoardPresenterTestCase(unittest.TestCase):
    def test_make_move(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        # Test a valid move
        try:
            presenter.make_move("e4")
        except Exception as e:
            self.fail(f"test_make_move raised {e}")

        # Illegal move
        with self.assertRaises(ValueError):
            presenter.make_move("O-O-O")

    def test_apply_file_labels(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        # Test with board coordinates disabled
        board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "no")
        self.assertEqual(presenter.apply_file_labels(), "")

        # Enable board coordinates
        board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "yes")
        board_config.set_value(board_config.Keys.FILE_LABEL_COLOR, "gray")

        # Test white board orientation
        model.set_board_orientation("white")
        expected_output = "<style fg='gray'>  a b c d e f g h </style>"
        self.assertEqual(presenter.apply_file_labels(), expected_output)

        # Test black board orientation
        model.set_board_orientation("black")
        expected_output = "<style fg='gray'>  h g f e d c b a </style>"
        self.assertEqual(presenter.apply_file_labels(), expected_output)

    def test_apply_rank_label(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        white_orientation_starting_squares = [chess.A1, chess.A2, chess.A3, chess.A4,
                                              chess.A5, chess.A6, chess.A7, chess.A8]
        black_orientation_starting_squares = [chess.H8, chess.H7, chess.H6, chess.H5,
                                              chess.H4, chess.H3, chess.H2, chess.H1]

        # Test with board coordinates disabled
        board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "no")
        for square in range(chess.A1, len(chess.SQUARES)):
            self.assertEqual(presenter.apply_rank_label(square), "")

        # Enable board coordinates
        board_config.set_value(board_config.Keys.SHOW_BOARD_COORDINATES, "yes")
        board_config.set_value(board_config.Keys.FILE_LABEL_COLOR, "gray")

        # Test white and black board orientations
        for square in range(chess.A1, len(chess.SQUARES)):
            square_rank_index = model.get_square_rank_index(square)
            rank_label = model.get_rank_label(square_rank_index)

            # Test white orientation
            model.set_board_orientation("white")

            if square in white_orientation_starting_squares:
                expected_output = f"<style fg='gray'> {rank_label}</style>"
                self.assertEqual(presenter.apply_rank_label(square), expected_output)
            else:
                self.assertEqual(presenter.apply_rank_label(square), "")

            # Test black orientation
            model.set_board_orientation("black")
            if square in black_orientation_starting_squares:
                expected_output = f"<style fg='gray'> {rank_label}</style>"
                self.assertEqual(expected_output, presenter.apply_rank_label(square))
            else:
                self.assertEqual(presenter.apply_rank_label(square), "")

    def test_get_square_final_display(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        # Set and obtain colors
        board_config.set_value(board_config.Keys.LIGHT_SQUARE_COLOR, "cadetblue")
        board_config.set_value(board_config.Keys.DARK_SQUARE_COLOR, "darkslateblue")
        board_config.set_value(board_config.Keys.LIGHT_PIECE_COLOR, "white")
        board_config.set_value(board_config.Keys.DARK_PIECE_COLOR, "black")
        light_square_color = board_config.get_value(board_config.Keys.LIGHT_SQUARE_COLOR)
        dark_square_color = board_config.get_value(board_config.Keys.DARK_SQUARE_COLOR)
        light_piece_color = board_config.get_value(board_config.Keys.LIGHT_PIECE_COLOR)
        dark_piece_color = board_config.get_value(board_config.Keys.DARK_PIECE_COLOR)

        for square in range(chess.A1, len(chess.SQUARES)):
            piece = model.board.piece_at(square)
            square_color = ""
            piece_color = ""

            if model.is_light_square(square):
                square_color = light_square_color
            elif not model.is_light_square(square):
                square_color = dark_square_color

            if piece:
                if piece.color == chess.WHITE:
                    piece_color = light_piece_color
                elif piece.color == chess.BLACK:
                    piece_color = dark_piece_color

                # Test blindfold mode
                board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "yes")
                expected_output = f"<style bg='{square_color}'>  </style>"
                self.assertEqual(presenter.get_square_final_display(square), expected_output)
                board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "no")

                # Test letter piece
                board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
                piece_character = piece.symbol()
                expected_output = f"<style fg='{piece_color}' bg='{square_color}'><b>{piece_character} </b></style>"
                self.assertEqual(presenter.get_square_final_display(square), expected_output)

                # Test unicode piece
                board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
                piece_character = get_piece_unicode_symbol(piece.symbol())
                expected_output = f"<style fg='{piece_color}' bg='{square_color}'><b>{piece_character} </b></style>"
                self.assertEqual(presenter.get_square_final_display(square), expected_output)
            else:
                # Test square that doesn't have a piece on it
                expected_output = f"<style bg='{square_color}'>  </style>"
                self.assertEqual(presenter.get_square_final_display(square), expected_output)

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

        defined_light_piece_color = board_config.get_value(board_config.Keys.LIGHT_PIECE_COLOR)
        defined_dark_piece_color = board_config.get_value(board_config.Keys.DARK_PIECE_COLOR)

        # Test light pieces
        for square in range(chess.A1, chess.H2):
            piece = model.board.piece_at(square)
            self.assertEqual(presenter.get_piece_color(piece), defined_light_piece_color)

        # Test dark pieces
        for square in range(chess.A7, chess.H8):
            piece = model.board.piece_at(square)
            self.assertEqual(presenter.get_piece_color(piece), defined_dark_piece_color)

        # Test empty squares
        for square in range(chess.A3, chess.H6):
            piece = model.board.piece_at(square)
            self.assertEqual(presenter.get_piece_color(piece), "")

    def test_get_square_display_color(self):
        model = BoardModel()
        presenter = BoardPresenter(model)

        # Set and obtain colors
        board_config.set_value(board_config.Keys.LIGHT_SQUARE_COLOR, "cadetblue")
        board_config.set_value(board_config.Keys.DARK_SQUARE_COLOR, "darkslateblue")
        board_config.set_value(board_config.Keys.IN_CHECK_COLOR, "red")
        board_config.set_value(board_config.Keys.LAST_MOVE_COLOR, "yellowgreen")
        light_square_color = board_config.get_value(board_config.Keys.LIGHT_SQUARE_COLOR)
        dark_square_color = board_config.get_value(board_config.Keys.DARK_SQUARE_COLOR)
        in_check_color = board_config.get_value(board_config.Keys.IN_CHECK_COLOR)
        last_move_color = board_config.get_value(board_config.Keys.LAST_MOVE_COLOR)

        model.board.set_fen("rnbqkbnr/ppppp1pp/8/5p2/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        model.make_move("Qh5")  # black in check
        last_move = model.board.peek()

        for square in range(chess.A1, len(chess.SQUARES)):
            if model.is_square_in_check(square):
                self.assertEqual(presenter.get_square_display_color(square), in_check_color)
            elif square == last_move.to_square or square == last_move.from_square:
                self.assertEqual(presenter.get_square_display_color(square), last_move_color)
            elif model.is_light_square(square):
                self.assertEqual(presenter.get_square_display_color(square), light_square_color)
            elif not model.is_light_square(square):
                self.assertEqual(presenter.get_square_display_color(square), dark_square_color)
            else:
                self.fail("Unexpected case caught")

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
