from .config import config
import chess

class BoardDisplay:
    '''Class to manage a chess boards display'''
    def __init__(self):
        '''Initialize the class'''
        self.board = chess.Board()
        self.perspective = self.set_board_perspective()
        self.square_numbers = self.get_square_numbers()


    def set_board_perspective(self):
        '''Returns the perspective of the board to display'''
        return "white"


    def perspective_is_white(self):
        '''Returns True is the board perspective is set as "white"'''
        if self.perspective == "black":
            return True
        else:
            return False


    def get_square_numbers(self):
        '''Returns the square numbers in a list based on board orientation'''
        square_numbers = []
        square_names = []

        for rank in range(len(chess.RANK_NAMES)-1, -1, -1):
            for file in range(len(chess.FILE_NAMES)):
                square_index = chess.square(file, rank)
                square_names.append(chess.square_name(square_index))
                square_numbers.append(chess.square(file, rank))

        if self.perspective_is_white():
            return square_numbers
        else:
            return square_numbers[::-1]


    def get_rank_names(self):
        '''Return the rank name list based on board perspective'''
        if self.perspective_is_white():
            return chess.RANK_NAMES[::-1]
        else:
            return chess.RANK_NAMES


    def get_file_names(self):
        '''Return the file name list based on board perspective'''
        if self.perspective_is_white():
            return chess.FILE_NAMES
        else:
            return chess.FILE_NAMES[::-1]


    def draw_board(self):
        '''Draws the chess board'''
        rank_count = 0
        count = 0
        new_line = True
        board_output = ""
        rank_names = self.get_rank_names()
        file_names = self.get_file_names()
        show_board_coordinates = config.get_board_boolean(config.BoardKeys.SHOW_BOARD_COORDINATES)
        use_unicode_pieces = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for square in self.square_numbers:
            if show_board_coordinates and new_line:
                board_output += rank_names[rank_count] + " "

            piece = self.board.piece_at(square)
            if piece:
                if use_unicode_pieces:
                    board_output += piece.unicode_symbol() + " "
                else:
                    board_output += piece.symbol() + " "
            else:
                board_output += ". "

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
            for file_name in file_names:
                board_output += file_name + " "
        print(board_output)
