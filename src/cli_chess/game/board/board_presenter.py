from . import BoardModel, BoardView
from cli_chess import config

board_keys = config.BoardKeys

UNICODE_PIECE_SYMBOLS = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",
}

class BoardPresenter:
    def __init__(self, model : BoardModel) -> None:
        self.board_model = model
        self.board_view = BoardView(self)
        self.board_output = self.update_board()


    def get_view(self):
        """Return the board view"""
        return self.board_view


    def make_move(self, move) -> str:
        """Make a move on the chess board. On a valid move, returns the move
           as a string. Otherwise, raises a ValueError on an illegal move.
        """
        try:
            move = self.board_model.make_move(move)

            #TODO: Wrap this in a move push function?
            self.update_board()
            return move

        except Exception:
            raise ValueError(f"Illegal move: {move}")


    def update_board(self):
        """Updates the board output (top left to bottom right) based
           on orientation and sends it to the view for display
        """
        board_output = ""
        board_squares = self.board_model.get_board_squares()
        for square in board_squares:
            board_output += self.apply_rank_label(square)
            board_output += self.get_square_final_display(square)
            board_output += self.start_new_line(square)

        board_output += self.apply_file_labels()
        self.board_output = board_output
        self.board_view.update(self.board_output)


    def apply_file_labels(self) -> str:
        """Returns a HTML string containing the file labels
           depending on the rank index and configuration settings
        """
        file_labels = ""
        show_board_coordinates = config.get_board_boolean(board_keys.SHOW_BOARD_COORDINATES)

        if show_board_coordinates:
            file_labels = self.board_model.get_file_labels()
            color = config.get_board_value(board_keys.FILE_LABEL_COLOR)
            file_labels = f"<style fg='{color}'>  {file_labels}</style>"

        return file_labels


    def apply_rank_label(self, square) -> str:
        """Returns a HTML formatted string with
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

        show_board_coordinates = config.get_board_boolean(board_keys.SHOW_BOARD_COORDINATES)

        if starting_index and show_board_coordinates:
            rank_label = " " + self.board_model.get_rank_label(rank_index)
            color = config.get_board_value(board_keys.RANK_LABEL_COLOR)
            rank_label = f"<style fg='{color}'>{rank_label}</style>"

        return rank_label


    def get_piece_unicode_symbol(self, symbol) -> str:
        """Returns the unicode symbol associated to the symbol passed in"""
        unicode_symbol = ""
        symbol = symbol.lower()
        if symbol in UNICODE_PIECE_SYMBOLS:
            unicode_symbol = UNICODE_PIECE_SYMBOLS[symbol]

        return unicode_symbol


    def get_square_final_display(self, square) -> str:
        """Returns a HTML string containing the final display for the passed in
           square. This includes the square color, and piece within the square.
        """
        piece = self.board_model.board.piece_at(square)
        square_color = self.get_square_display_color(square)
        square_output = ""

        blindfold_chess = config.get_board_boolean(board_keys.BLINDFOLD_CHESS)
        use_unicode_pieces = config.get_board_boolean(board_keys.USE_UNICODE_PIECES)

        if piece and not blindfold_chess:
            piece_color = self.get_piece_color(piece)
            piece_character = self.get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol()
            square_output = f"<style fg='{piece_color}' bg='{square_color}'><b>{piece_character} </b></style>"
        else:
            square_output = f"<style bg='{square_color}'>  </style>"

        return square_output


    def start_new_line(self, square) -> str:
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


    def get_piece_color(self, piece) -> str:
        """Returns a string with the color to display the
           piece based on configuration settings
        """
        piece_color = ""

        if piece:
            piece_is_light = piece.color == True
            if piece_is_light:
                piece_color = config.get_board_value(board_keys.LIGHT_PIECE_COLOR)
            else:
                piece_color = config.get_board_value(board_keys.DARK_PIECE_COLOR)

        return piece_color


    def get_square_display_color(self, square) -> str:
        """Returns a string with the color to display the
           square based on configuration settings, last move, and check.
        """
        square_color = ""
        if self.board_model.is_light_square(square):
            square_color = config.get_board_value(board_keys.LIGHT_SQUARE_COLOR)
        else:
            square_color = config.get_board_value(board_keys.DARK_SQUARE_COLOR)

        show_board_highlights = config.get_board_boolean(board_keys.SHOW_BOARD_HIGHLIGHTS)
        if show_board_highlights:
            try:
                last_move = self.board_model.board.peek()
                if square == last_move.to_square or square == last_move.from_square:
                    square_color = config.get_board_value(board_keys.LAST_MOVE_COLOR)
                    #TODO: Lighten last move color if on light square
            except:
                pass

            if self.board_model.is_square_in_check(square):
                square_color = config.get_board_value(board_keys.IN_CHECK_COLOR)

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
