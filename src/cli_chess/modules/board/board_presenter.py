from __future__ import annotations
from cli_chess.modules.board import BoardView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import game_config
import chess
from typing import List, Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.board import BoardModel


class BoardPresenter:
    def __init__(self, model: BoardModel) -> None:
        self.model = model
        self.game_config_values = game_config.get_all_values()
        self.view = BoardView(self, self.get_board_display())

        self.model.e_board_model_updated.add_listener(self.update)
        game_config.e_game_config_updated.add_listener(self._update_cached_config_values)

    def update(self, *args, **kwargs) -> None: # noqa
        """Updates the board output"""
        # TODO: Update this so the view utilizes a lambda pointing to the presenter?
        #       This would allow for this update function to be removed
        self.view.update(self.get_board_display())

    def _update_cached_config_values(self):
        """Updates the 'game_config_values' variable with the
           latest configuration values from the game_config. Additionally,
           this will notify the board_view to update as there has been a change.
           This function is called automatically on game config updates
        """
        self.game_config_values = game_config.get_all_values()
        self.update()

    def make_move(self, move: str) -> None:
        """Sends a move to the board model to attempt to make.
           Raises a ValueError on invalid moves. See model for specifics.
        """
        try:
            self.model.make_move(move)
        except ValueError as e:
            raise e

    def get_board_display(self) -> List[Dict]:
        """Returns a list containing the complete board display. Each item in the list
           is a dictionary containing the display data for that square (piece at,
           piece color, square color, square number, etc). This data is generally sent
           to the view to output the board display.
        """
        board_output = []
        board_squares = self.model.get_board_squares()

        # TODO: Update this implementation to use a dictionary so
        #       the following syntax can be used: board_output[chess.D2]?
        for square in board_squares:
            data = {'square_number': square,
                    'piece_str': self.get_piece_str(square),
                    'piece_display_color': self.get_piece_display_color(self.model.board.piece_at(square)),
                    'square_display_color': self.get_square_display_color(square),
                    'rank_label': self.get_rank_label(square),
                    'is_end_of_rank': self.is_square_end_of_rank(square)}
            board_output.append(data)

        return board_output

    def get_file_labels(self) -> str:
        """Returns a string containing the file labels. An empty
           string will be returned if showing the board coordinates
           is disabled in the configuration.
        """
        file_labels = ""
        show_board_coordinates = self.game_config_values[game_config.Keys.SHOW_BOARD_COORDINATES]

        if show_board_coordinates:
            file_labels = self.model.get_file_labels()

        return file_labels

    def get_rank_label(self, square: chess.Square) -> str:
        """Returns a label string if at the start of a rank
           otherwise an empty string will be returned
        """
        rank_label = ""
        rank_index = self.model.get_square_rank_index(square)
        show_board_coordinates = self.game_config_values[game_config.Keys.SHOW_BOARD_COORDINATES]

        if self.is_square_start_of_rank(square) and show_board_coordinates:
            rank_label = self.model.get_rank_label(rank_index)

        return rank_label

    def is_square_start_of_rank(self, square: chess.Square) -> bool:
        """Returns True if the square passed in is the start of a rank"""
        is_start_of_rank = False

        if self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_A:
            is_start_of_rank = True
        elif not self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_H:
            is_start_of_rank = True

        return is_start_of_rank

    def is_square_end_of_rank(self, square: chess.Square) -> bool:
        """Returns True if the square passed in is the last on the rank"""
        is_end_of_rank = False

        if self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_H:
            is_end_of_rank = True
        elif not self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_A:
            is_end_of_rank = True

        return is_end_of_rank

    def get_piece_str(self, square: chess.Square):
        """Returns the piece at the square as a string. Depending on configuration
           settings, this could be a unicode character, a letter, or an empty
           string if blindfold chess is enabled in the configuration, or there is
           not a piece at the square
        """
        piece = self.model.board.piece_at(square)
        piece_str = ""

        blindfold_chess = self.game_config_values[game_config.Keys.BLINDFOLD_CHESS]
        use_unicode_pieces = self.game_config_values[game_config.Keys.USE_UNICODE_PIECES]

        if piece and not blindfold_chess:
            piece_str = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol().upper()

        return piece_str

    @staticmethod
    def get_piece_display_color(piece: chess.Piece) -> str:
        """Returns a string with the color to display the
           piece based on configuration settings
        """
        piece_color = ""

        if piece:
            piece_is_light = True if piece.color else False
            if piece_is_light:
                piece_color = "light-piece"
            else:
                piece_color = "dark-piece"

        return piece_color

    def get_square_display_color(self, square: chess.Square) -> str:
        """Returns a string with the color to display the
           square based on configuration settings, last move, and check.
        """
        if self.model.is_light_square(square):
            square_color = "light-square"
        else:
            square_color = "dark-square"

        show_board_highlights = self.game_config_values[game_config.Keys.SHOW_BOARD_HIGHLIGHTS]
        if show_board_highlights:
            # TODO: Lighten last move square color if on light square
            try:
                last_move = self.model.get_highlight_move()
                if bool(last_move) and (square == last_move.to_square or square == last_move.from_square):
                    square_color = "last-move"

                premove_highlight = self.model.premove_highlight
                if bool(premove_highlight) and (square == premove_highlight.from_square or square == premove_highlight.to_square):
                    square_color = "pre-move"
            except IndexError:
                pass

            if self.model.is_square_in_check(square):
                square_color = "in-check"

        return square_color

    def handle_resignation(self, color_resigning: chess.Color) -> None:
        """Handle marking the game as ended by resignation. Sends the
           resignation notification over to the model to be handled.
        """
        self.model.handle_resignation(color_resigning)
