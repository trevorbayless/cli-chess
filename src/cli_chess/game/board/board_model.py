import chess
import chess.variant


class BoardModel:
    def __init__(self, orientation="white", variant="Standard", fen=None) -> None:
        if not fen:
            fen = chess.variant.find_variant(variant).starting_fen

        self.board = chess.variant.find_variant(variant)(fen)
        self.board_orientation = orientation


    def make_move(self, move) -> chess.Move:
        """Makes a move on the board"""
        return self.board.push_san(move)


    def set_board_orientation(self, orientation) -> None:
        """Sets the board orientation"""
        self.board_orientation = orientation


    def get_board_orientation(self) -> str:
        """Returns the board orientation as a string"""
        return self.board_orientation


    def get_board_squares(self) -> list:
        """Returns the boards square numbers as a list based current orientation"""
        square_numbers = []
        square_names = []

        for rank in range(len(chess.RANK_NAMES)-1, -1, -1):
            for file in range(len(chess.FILE_NAMES)):
                square_index = chess.square(file, rank)
                square_names.append(chess.square_name(square_index))
                square_numbers.append(chess.square(file, rank))

        if self.board_orientation == "black":
            return square_numbers[::-1]

        return square_numbers


    def get_square_file_index(self, square) -> int:
        """Returns the file index of the passed in square"""
        return chess.square_file(square)


    def get_file_labels(self) -> str:
        """Returns a string containing the file
           labels based on the board orientation
        """
        file_labels = ""
        if self.board_orientation == "black":
            for name in chess.FILE_NAMES[::-1]:
                file_labels += name + " "
        else:
            for name in chess.FILE_NAMES:
                file_labels += name + " "

        return file_labels


    def get_square_rank_index(self, square) -> int:
        """Returns the rank index of the passed in square"""
        return chess.square_rank(square)


    def get_rank_label(self, rank_index) -> str:
        """Returns the rank label at the index passed in"""
        return chess.RANK_NAMES[rank_index]


    def is_square_in_check(self, square) -> bool:
        """Returns True if a king who's turn it is
           is in check as the passed in square
        """
        king_square = self.board.king(self.board.turn)
        if square == king_square and self.board.is_check():
            return True
        return False


    def is_white_orientation(self) -> bool:
        """Returns True if the board orientation is set as white"""
        if self.board_orientation == "white":
            return True
        else:
            return False
