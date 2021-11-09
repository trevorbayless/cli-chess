import chess.variant
from chess import Move, Board
from typing import Type

class BoardModel:
    def __init__(self, orientation="white", variant="Standard", fen=None) -> None:
        if not fen:
            fen = chess.variant.find_variant(variant).starting_fen

        self.board = chess.variant.find_variant(variant)(fen)
        self.board_orientation = orientation


    def make_move(self, move) -> Move:
        """Makes a move on the board"""
        return self.board.push_san(move)


    def set_board_orientation(self, orientation) -> None:
        """Sets the board orientation"""
        self.board_orientation = orientation


    def get_board_orientation(self) -> str:
        """Returns the board orientation as a string"""
        return self.board_orientation


    def get_board(self) -> Type[Board]:
        """Returns the board object"""
        return self.board


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


    def get_piece_at_square(self, square):
        """Returns the piece at the passed in square"""
        return self.board.piece_at(square)


    def get_square_file(self, square):
        """Returns the file of the passed in square"""
        return chess.square_file(square)


    def get_square_rank(self, square):
        """Returns the rank of the passed in square"""
        return chess.square_rank(square)


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


    def get_rank_label(self, square) -> str:
        """Returns the rank label as a string based on the square passed in"""
        rank_label = ""
        starting_index = False

        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        if self.is_white_orientation() and file_index == 0:
            starting_index = True
        elif not self.is_white_orientation() and file_index == 7:
            starting_index = True

        if starting_index:
            rank_label = chess.RANK_NAMES[rank_index] + " "

        return rank_label


    def get_previous_move(self):
        """Returns the previous move"""
        return self.board.peek()


    def is_square_in_check(self, square) -> bool:
        """Returns True if a king who's turn it is
           is in check as the passed in square
        """
        if self.board.is_check() or self.board.is_checkmate():
            piece = self.board.piece_at(square)
            if piece:
                is_king_piece = piece.piece_type == chess.KING
                proper_turn = piece.color == self.board.turn

                if is_king_piece and proper_turn:
                    return True
        return False


    def is_white_orientation(self) -> bool:
        """Returns True if the board orientation is set as white"""
        if self.board_orientation == "white":
            return True
        else:
            return False


    def get_game_over_result(self) -> str:
        """Returns a string with the game over result"""
        return self.board.result()


    def is_checkmate(self):
        """Returns True if the current position is checkmate"""
        return self.board.is_checkmate()


    def is_stalemate(self):
        """Returns true if the current position is stalemate"""
        return self.board.is_stalemate()
