import chess
import chess.variant
from cli_chess.utils import Event


class BoardModel:
    def __init__(self, orientation="white", variant="Standard", fen=None) -> None:
        if not fen:
            fen = chess.variant.find_variant(variant).starting_fen

        self.initial_fen = fen
        self.board = chess.variant.find_variant(variant)(self.initial_fen)
        self.board_orientation = orientation
        self.e_board_model_updated = Event()


    def _board_model_updated(self) -> None:
        """Used to notify listeners of board model updates"""
        self.e_board_model_updated.notify()


    def make_move(self, move) -> None:
        """Attempts to make a move on the board.
           Raises a ValueError on illegal moves.
        """
        self.board.push_san(move)
        self._board_model_updated()


    def get_move_stack(self):
        """Returns the boards move stack"""
        return self.board.move_stack


    def get_initial_fen(self) -> str:
        """Returns a string holding the initial board fen"""
        return self.initial_fen


    def get_variant_name(self) -> str:
        """Returns a string holding the board variant name"""
        return self.board.uci_variant


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


    def is_light_square(self, square) -> bool:
        """Returns True if the square passed in is a light square"""
        if square in chess.SQUARES:
            file_index = self.get_square_file_index(square)
            rank_index = self.get_square_rank_index(square)

            return (file_index % 2) != (rank_index % 2)
        else:
            raise(ValueError(f"Illegal square: {square}"))


    def is_white_orientation(self) -> bool:
        """Returns True if the board orientation is set as white"""
        if self.board_orientation == "white":
            return True
        else:
            return False
