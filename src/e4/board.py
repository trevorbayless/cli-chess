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
    else:
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


    def add_rank_label(self, rank_index, new_line):
        '''Add a rank label if needed'''
        rank_label = ""
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)
        if show_board_coordinates and new_line:
            rank_label = chess.RANK_NAMES[rank_index] + " "
        return rank_label


    def add_file_labels(self):
        '''Add a fiel labels if needed'''
        file_names = "  "
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)
        if show_board_coordinates:
            if self.orientation == "black":
                for file_name in chess.FILE_NAMES[::-1]:
                    file_names += file_name + " "
            else:
                for file_name in chess.FILE_NAMES:
                    file_names += file_name + " "
        return file_names


    def draw_board(self):
        '''Draws the board (top left to bottom right) based on stored positions and orientation'''
        rank_count = 0
        count = 0
        new_line = True
        board_output = ""
        blindfold_chess = config.get_board_boolean(config.BoardKeys.BLINDFOLD_CHESS)
        use_unicode_pieces = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for square in self.square_numbers:
            file_index = chess.square_file(square)
            rank_index = chess.square_rank(square)
            square_color = self.get_square_display_color(file_index, rank_index)

            board_output += self.add_rank_label(rank_index, new_line)

            piece = self.board.piece_at(square)
            if piece and not blindfold_chess:
                piece_display = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol()
                piece_color = self.get_piece_display_color(piece)
                board_output += f"<style fg='{piece_color}' bg='{square_color}'>{piece_display} </style>"
            else:
                board_output += f"<style bg='{square_color}'>  </style>"

            if count >= len(chess.FILE_NAMES) - 1:
                board_output += "\n"
                count = 0
                rank_count += 1
                new_line = True

            else:
                count += 1
                new_line = False

        board_output += self.add_file_labels()

        print(HTML(board_output + "\n"))
