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

from . import BoardModel, BoardView
from cli_chess.game.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
from chess import Piece, Square


class BoardPresenter:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_config_values = board_config.get_all_values()
        self.view = BoardView(self, self.build_board_output())
        self.board_model.e_board_model_updated.add_listener(self.update)

    def update(self) -> None:
        """Updates the board output"""
        self.board_config_values = board_config.get_all_values()
        self.view.update(self.build_board_output())

    def make_move(self, move: str, human=True) -> None:
        """Sends a move to the board model to attempt to make.
           Raises an exception on invalid moves
        """
        try:
            self.board_model.make_move(move, human=human)
        except Exception as e:
            # TODO: Handle specific exceptions (Invalid move, ambiguous, etc )
            raise e

    def build_board_output(self) -> str:
        """Builds the board output (top left to bottom right) based
           on orientation. Returns a string containing the board.
        """
        board_output = ""
        board_squares = self.board_model.get_board_squares()
        for square in board_squares:
            board_output += self.apply_rank_label(square)
            board_output += self.get_square_final_display(square)
            board_output += self.start_new_line(square)

        board_output += self.apply_file_labels()
        return board_output

    def apply_file_labels(self) -> str:
        """Returns an HTML string containing the file labels
           depending on the rank index and configuration settings
        """
        file_labels = ""
        show_board_coordinates = self.board_config_values[board_config.Keys.SHOW_BOARD_COORDINATES.name.lower()]

        if show_board_coordinates:
            file_labels = self.board_model.get_file_labels()
            color = self.board_config_values[board_config.Keys.FILE_LABEL_COLOR.name.lower()]
            file_labels = f"<style fg='{color}'>  {file_labels}</style>"

        return file_labels

    def apply_rank_label(self, square: Square) -> str:
        """Returns an HTML formatted string with
           the rank label at the square passed in.
        """
        rank_label = ""
        starting_index = False
        file_index = self.board_model.get_square_file_index(square)
        rank_index = self.board_model.get_square_rank_index(square)

        if self.board_model.is_white_orientation() and file_index == 0:
            starting_index = True
        elif not self.board_model.is_white_orientation() and file_index == 7:
            starting_index = True

        show_board_coordinates = self.board_config_values[board_config.Keys.SHOW_BOARD_COORDINATES.name.lower()]

        if starting_index and show_board_coordinates:
            rank_label = " " + self.board_model.get_rank_label(rank_index)
            color = self.board_config_values[board_config.Keys.RANK_LABEL_COLOR.name.lower()]
            rank_label = f"<style fg='{color}'>{rank_label}</style>"

        return rank_label

    def get_square_final_display(self, square: Square) -> str:
        """Returns a HTML string containing the final display for the passed in
           square. This includes the square color, and piece within the square.
        """
        piece = self.board_model.board.piece_at(square)
        square_color = self.get_square_display_color(square)

        blindfold_chess = self.board_config_values[board_config.Keys.BLINDFOLD_CHESS.name.lower()]
        use_unicode_pieces = self.board_config_values[board_config.Keys.USE_UNICODE_PIECES.name.lower()]

        if piece and not blindfold_chess:
            piece_color = self.get_piece_color(piece)
            piece_character = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol()
            square_output = f"<style fg='{piece_color}' bg='{square_color}'>{piece_character} </style>"
        else:
            square_output = f"<style bg='{square_color}'>  </style>"

        return square_output

    def start_new_line(self, square: Square) -> str:
        """Returns a new line if the board output needs to start on a new
           line based on the board orientation and file index
        """
        output = ""
        file_index = self.board_model.get_square_file_index(square)

        if self.board_model.is_white_orientation() and file_index == 7:
            output = "\n"
        elif not self.board_model.is_white_orientation() and file_index == 0:
            output = "\n"

        return output

    def get_piece_color(self, piece: Piece) -> str:
        """Returns a string with the color to display the
           piece based on configuration settings
        """
        piece_color = ""

        if piece:
            piece_is_light = True if piece.color else False
            if piece_is_light:
                piece_color = self.board_config_values[board_config.Keys.LIGHT_PIECE_COLOR.name.lower()]
            else:
                piece_color = self.board_config_values[board_config.Keys.DARK_PIECE_COLOR.name.lower()]

        return piece_color

    def get_square_display_color(self, square) -> str:
        """Returns a string with the color to display the
           square based on configuration settings, last move, and check.
        """
        if self.board_model.is_light_square(square):
            square_color = self.board_config_values[board_config.Keys.LIGHT_SQUARE_COLOR.name.lower()]
        else:
            square_color = self.board_config_values[board_config.Keys.DARK_SQUARE_COLOR.name.lower()]

        show_board_highlights = self.board_config_values[board_config.Keys.SHOW_BOARD_HIGHLIGHTS.name.lower()]
        if show_board_highlights:
            try:
                last_move = self.board_model.board.peek()
                if square == last_move.to_square or square == last_move.from_square:
                    square_color = self.board_config_values[board_config.Keys.LAST_MOVE_COLOR.name.lower()]
                    # TODO: Lighten last move color if on light square
            except IndexError:
                pass

            if self.board_model.is_square_in_check(square):
                square_color = self.board_config_values[board_config.Keys.IN_CHECK_COLOR.name.lower()]

        return square_color

    def game_result(self) -> str:
        """Returns a string containing the result of the game"""
        game_result = self.board_model.board.result()
        is_checkmate = self.board_model.board.is_checkmate()
        output = ""

        if is_checkmate:
            output = "Checkmate - "
        if game_result == "1-0":
            output += "White is victorious"
        elif game_result == "0-1":
            output += "Black is victorious"
        elif game_result == "1/2-1/2":
            if self.board_model.board.is_stalemate():
                output = "Stalemate"
            else:
                output = "Draw"
        elif game_result == "*":
            output = "Draw"

        return output
