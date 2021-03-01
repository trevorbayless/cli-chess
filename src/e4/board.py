import chess
from .config import config
from prompt_toolkit import HTML, print_formatted_text as print

UNICODE_PIECE_SYMBOLS = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",
}

def get_square_numbers(orientation):
    '''Returns the square numbers as a list based on board orientation'''
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


class BoardBase:
    '''Base board class'''
    def __init__(self, orientation, fen=chess.STARTING_FEN):
        self.board = chess.Board(fen)
        self.orientation = orientation
        self.square_numbers = get_square_numbers(self.orientation)


    def set_orientation(self, orientation):
        '''Sets the board orientation'''
        self.orientation = orientation


    def is_white_orientation(self):
        '''Returns true if the board orientation is set as white'''
        if self.orientation == "white":
            return True
        else:
            return False


    def get_piece_display_color(self, piece):
        '''Returns the color to display the piece as a string'''
        base_is_white = piece.color == True
        if base_is_white:
            return config.get_board_value(config.BoardKeys.LIGHT_PIECE_COLOR)
        else:
            return config.get_board_value(config.BoardKeys.DARK_PIECE_COLOR)


    def get_square_display_color(self, file_index, rank_index):
        '''Returns the color to display the square as a string'''
        is_light_square = (file_index % 2) != (rank_index % 2)
        if is_light_square:
            return config.get_board_value(config.BoardKeys.LIGHT_SQUARE_COLOR)
        else:
            return config.get_board_value(config.BoardKeys.DARK_SQUARE_COLOR)


class Board(BoardBase):
    '''Class to manage a chess board display'''
    def __init__(self, orientation, fen=chess.STARTING_FEN):
        '''Initialize the class'''
        super().__init__(orientation, fen)


    def draw_board(self):
        '''Draws the board (top left to bottom right) based on stored positions and orientation'''
        blindfold_chess = config.get_board_boolean(config.BoardKeys.BLINDFOLD_CHESS)
        use_unicode_pieces = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)
        board_output = ""

        for square in self.square_numbers:
            file_index = chess.square_file(square)
            rank_index = chess.square_rank(square)
            square_color = self.get_square_display_color(file_index, rank_index)
            piece = self.board.piece_at(square)
            square_output = ""

            if piece and not blindfold_chess:
                piece_color = self.get_piece_display_color(piece)
                piece_character = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol()
                square_output = f"<style fg='{piece_color}' bg='{square_color}'>{piece_character} </style>"
            else:
                square_output = f"<style bg='{square_color}'>  </style>"

            board_output += self.get_rank_label(file_index, rank_index)
            board_output += square_output
            board_output += self.start_new_line(file_index)

        board_output += self.get_file_labels() + "\n"

        print(HTML(board_output))


    def get_rank_label(self, file_index, rank_index):
        '''Add a rank label if needed'''
        rank_label = ""
        proper_file_index = False
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)

        if self.is_white_orientation() and file_index == 0:
            proper_file_index = True
        elif not self.is_white_orientation() and file_index == 7:
            proper_file_index = True

        if show_board_coordinates and proper_file_index:
            rank_label = chess.RANK_NAMES[rank_index] + " "

        return rank_label


    def get_file_labels(self):
        '''Returns a string containing the file labels depending
           on the rank index and configuration settings
        '''
        file_labels = ""
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)

        if show_board_coordinates:
            file_labels = "  "
            if self.orientation == "black":
                for name in chess.FILE_NAMES[::-1]:
                    file_labels += name + " "
            else:
                for name in chess.FILE_NAMES:
                    file_labels += name + " "

        return file_labels


    def start_new_line(self, file_index):
        '''Returns a new line if the board output needs to start on a new
           line based on the board orientation and file index
        '''
        output = ""
        if self.is_white_orientation() and file_index == 7:
            output = "\n"
        elif not self.is_white_orientation() and file_index == 0:
            output = "\n"

        return output
