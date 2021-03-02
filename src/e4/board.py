import chess
from .config import config
from prompt_toolkit import HTML, print_formatted_text as print
from prompt_toolkit.output import ColorDepth

board_keys = config.BoardKeys

UNICODE_PIECE_SYMBOLS = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",
}

def get_board_squares(orientation):
    '''Returns the boards square numbers as a list based on board orientation'''
    square_numbers = []
    square_names = []

    for rank in range(len(chess.RANK_NAMES)-1, -1, -1):
        for file in range(len(chess.FILE_NAMES)):
            square_index = chess.square(file, rank)
            square_names.append(chess.square_name(square_index))
            square_numbers.append(chess.square(file, rank))

    if orientation == "black":
        return square_numbers[::-1]

    return square_numbers


def get_piece_unicode_symbol(symbol):
    '''Returns the unicode symbol associated to the symbol passed in'''
    return UNICODE_PIECE_SYMBOLS[symbol.lower()]


class Board:
    '''Class to manage a chess board display'''
    def __init__(self, orientation, fen=chess.STARTING_FEN):
        '''Initialize the class'''
        self.board = chess.Board(fen)
        self.board_orientation = orientation
        self.board_squares = get_board_squares(self.board_orientation)
        self.board_display = self.generate_board()


    def generate_board(self):
        '''Generates and returns the board as a HTML string (top left to bottom right)
           based on the board orientation, and stored piece positions
        '''
        board_output = ""
        for square in self.board_squares:
            board_output += self.get_rank_label(square)
            board_output += self.get_squares_final_display(square)
            board_output += self.start_new_line(square)

        board_output += self.get_file_labels() + "\n"

        return board_output


    def print_board(self):
        '''Prints the board'''
        print(HTML(self.board_display), color_depth=ColorDepth.TRUE_COLOR)


    def get_squares_final_display(self, square):
        '''Returns as a HTML string containing the final display for the passed in square.
           This includes the square color, and piece within the square.
        '''
        piece = self.board.piece_at(square)
        square_color = self.get_square_color(square)
        square_output = ""

        blindfold_chess = config.get_board_boolean(board_keys.BLINDFOLD_CHESS)
        use_unicode_pieces = config.get_board_boolean(board_keys.USE_UNICODE_PIECES)

        if piece and not blindfold_chess:
            piece_color = self.get_piece_color(piece)
            piece_character = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol()
            square_output = f"<style fg='{piece_color}' bg='{square_color}'>{piece_character} </style>"
        else:
            square_output = f"<style bg='{square_color}'>  </style>"

        return square_output


    def get_piece_color(self, piece):
        '''Returns a string with the color to display the
           piece as based on configuration settings
        '''
        piece_color = ""
        base_is_white = piece.color == True
        if base_is_white:
            piece_color = config.get_board_value(board_keys.LIGHT_PIECE_COLOR)
        else:
            piece_color = config.get_board_value(board_keys.DARK_PIECE_COLOR)

        return piece_color


    def get_square_color(self, square):
        '''Returns a string with the color to display the
           square based on configuration settings
        '''
        square_color = ""
        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        is_light_square = (file_index % 2) != (rank_index % 2)
        if is_light_square:
            square_color = config.get_board_value(board_keys.LIGHT_SQUARE_COLOR)
        else:
            square_color = config.get_board_value(board_keys.DARK_SQUARE_COLOR)

        show_board_highlights = config.get_board_boolean(board_keys.SHOW_BOARD_HIGHLIGHTS)
        if show_board_highlights:
            if self.square_in_check(square):
                square_color = config.get_board_value(board_keys.IN_CHECK_COLOR)

        return square_color


    def square_in_check(self, square):
        '''Returns True if a king who's turn it is
           is in check as the passed in square
        '''
        if self.board.is_check():
            piece = self.board.piece_at(square)
            if piece:
                is_king_piece = piece.piece_type == chess.KING
                proper_turn = piece.color == self.board.turn

                if is_king_piece and proper_turn:
                    return True
        return False


    def get_file_labels(self):
        '''Returns a string containing the file labels depending
           on the rank index and configuration settings
        '''
        file_labels = ""
        show_board_coordinates = config.get_board_boolean(board_keys.SHOW_BOARD_COORDINATES)

        if show_board_coordinates:
            file_labels = "  "
            if self.board_orientation == "black":
                for name in chess.FILE_NAMES[::-1]:
                    file_labels += name + " "
            else:
                for name in chess.FILE_NAMES:
                    file_labels += name + " "

        return file_labels


    def get_rank_label(self, square):
        '''Returns a string with the rank label at the
           square passed in. Return is based on '''
        rank_label = ""
        proper_file_index = False
        show_board_coordinates = config.get_board_boolean(board_keys.SHOW_BOARD_COORDINATES)

        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        if self.is_white_orientation() and file_index == 0:
            proper_file_index = True
        elif not self.is_white_orientation() and file_index == 7:
            proper_file_index = True

        if show_board_coordinates and proper_file_index:
            rank_label = chess.RANK_NAMES[rank_index] + " "

        return rank_label


    def start_new_line(self, square):
        '''Returns a new line if the board output needs to start on a new
           line based on the board orientation and file index
        '''
        output = ""
        file_index = chess.square_file(square)

        if self.is_white_orientation() and file_index == 7:
            output = "\n"
        elif not self.is_white_orientation() and file_index == 0:
            output = "\n"

        return output


    def is_white_orientation(self):
        '''Returns True if the board orientation is set as white'''
        if self.board_orientation == "white":
            return True
        else:
            return False
