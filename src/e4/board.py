from .config import config
import chess

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


def get_file_names(orientation):
    '''Return the file names as a list based on board orientation'''
    if orientation == "white":
        return chess.FILE_NAMES
    else:
        return chess.FILE_NAMES[::-1]


def get_rank_names(orientation):
    '''Return the rank names as a list based on board orientation'''
    if orientation == "white":
        return chess.RANK_NAMES[::-1]
    else:
        return chess.RANK_NAMES


class BoardBase:
    '''Base board class'''
    def __init__(self, orientation, fen=chess.STARTING_FEN):
        self.board = chess.Board(fen)
        self.orientation = orientation
        self.square_numbers = get_square_numbers(self.orientation)
        self.file_names = get_file_names(self.orientation)
        self.rank_names = get_rank_names(self.orientation)


    def set_orientation(self, orientation):
        '''Sets the board orientation'''
        self.orientation = orientation


    def is_white_orientation(self):
        '''Returns true if the board orientation is set as white'''
        if self.orientation == "white":
            return True
        else:
            return False


class Board(BoardBase):
    '''Class to manage a chess board display'''
    def __init__(self, orientation, fen=chess.STARTING_FEN):
        '''Initialize the class'''
        super().__init__(orientation, fen)


    def draw_board(self):
        '''Draws the board based on stored positions'''
        rank_count = 0
        count = 0
        new_line = True
        board_output = ""
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)
        blindfold_mode = config.get_board_boolean(config.BoardKeys.BLINDFOLD_CHESS)
        use_unicode_pieces = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for square in self.square_numbers:
            if show_board_coordinates and new_line:
                board_output += self.rank_names[rank_count] + " "

            piece = self.board.piece_at(square)
            if piece:
                if not blindfold_mode:
                    if use_unicode_pieces:
                        board_output += piece.unicode_symbol() + " "
                    else:
                        board_output += piece.symbol() + " "
            else:
                board_output += "  "

            if count >= len(chess.FILE_NAMES) - 1:
                board_output += "\n"
                count = 0
                rank_count += 1
                new_line = True

            else:
                count += 1
                new_line = False

        if show_board_coordinates:
            board_output += "  "
            for file_name in self.file_names:
                board_output += file_name + " "

        print(board_output + "\n")
