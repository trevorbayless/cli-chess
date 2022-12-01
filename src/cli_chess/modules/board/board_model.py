# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from cli_chess.utils.event import Event
from cli_chess.utils.logging import log
from random import randint
from typing import List
import chess.variant
import chess


# Todo: Inherit from chess.Board?
class BoardModel:
    def __init__(self, my_color: chess.Color = chess.WHITE, variant: str = "standard", fen: str = "") -> None:
        self.board = self._initialize_board(variant, fen)
        self.my_color = my_color
        self.board_orientation = self.my_color

        self._log_init_info()
        self.e_board_model_updated = Event()
        self.e_successful_move_made = Event()

    @staticmethod
    def _initialize_board(variant, fen) -> chess.Board:
        """Initializes and returns the main board object"""
        if variant == "chess960":
            return chess.Board.from_chess960_pos(randint(0, 959))
        else:
            if fen:
                return chess.variant.find_variant(variant)(fen)
            return chess.variant.find_variant(variant)()

    def make_move(self, move: str, human=True) -> None:
        """Attempts to make a move on the board.
           Raises a ValueError on illegal moves.
        """
        player = "human" if human else "engine"
        try:
            move = move.strip()
            self.board.push_san(move)
            self._notify_successful_move_made()
            self._notify_board_model_updated()
            log.info(f"make_move ({player}): {move}")
        except Exception as e:
            log.error(f"make_move ({player}): {e}")
            raise e

    def takeback(self):
        """Takes back the last played move. Raises
           IndexError if the move stack is empty
        """
        try:
            self.board.pop()
            self._notify_board_model_updated()
            self._notify_successful_move_made()
        except IndexError as e:
            log.error(f"Error attempting takeback: {e}")
            raise e

    def get_move_stack(self) -> List[chess.Move]:
        """Returns the boards move stack"""
        return self.board.move_stack

    def get_variant_name(self) -> str:
        """Returns a string holding the board variant name"""
        if self.board.uci_variant == "chess" and self.board.chess960:
            return "chess960"
        else:
            return self.board.uci_variant

    def get_turn(self) -> chess.Color:
        """Returns the color of which turn it is"""
        return self.board.turn

    def get_board_orientation(self) -> chess.Color:
        """Returns the board orientation"""
        return self.board_orientation

    def set_board_orientation(self, color: chess.Color) -> None:
        """Sets the board's orientation to the color passed in"""
        self.board_orientation = color
        self._notify_board_model_updated()
        log.debug(f"board orientation set (orientation = {color}")

    def set_fen(self, fen: str) -> None:
        """Sets the board FEN. Raises ValueError if syntactically invalid"""
        try:
            self.board.set_fen(fen)
            self._notify_board_model_updated()
        except Exception as e:
            log.error(f"Error setting FEN: {e}")
            raise e

    def get_board_squares(self) -> list:
        """Returns the boards square numbers as a list based current board orientation"""
        # Square numbers from white perspective
        square_numbers = [56, 57, 58, 59, 60, 61, 62, 63,
                          48, 49, 50, 51, 52, 53, 54, 55,
                          40, 41, 42, 43, 44, 45, 46, 47,
                          32, 33, 34, 35, 36, 37, 38, 39,
                          24, 25, 26, 27, 28, 29, 30, 31,
                          16, 17, 18, 19, 20, 21, 22, 23,
                          8, 9, 10, 11, 12, 13, 14, 15,
                          0, 1, 2, 3, 4, 5, 6, 7]

        if self.board_orientation is chess.BLACK:
            return square_numbers[::-1]

        return square_numbers

    @staticmethod
    def get_square_file_index(square: chess.Square) -> int:
        """Returns the file index of the passed in square"""
        return chess.square_file(square)

    def get_file_labels(self) -> str:
        """Returns a string containing the file
           labels based on the board orientation'
        """
        file_labels = ""
        if self.board_orientation is chess.BLACK:
            for name in chess.FILE_NAMES[::-1]:
                file_labels += name + " "
        else:
            for name in chess.FILE_NAMES:
                file_labels += name + " "

        return file_labels

    @staticmethod
    def get_square_rank_index(square: chess.Square) -> int:
        """Returns the rank index of the passed in square"""
        return chess.square_rank(square)

    @staticmethod
    def get_rank_label(rank_index: int) -> str:
        """Returns the rank label at the index passed in"""
        return chess.RANK_NAMES[rank_index]

    def is_square_in_check(self, square: chess.Square) -> bool:
        """Returns True if a king whose turn it is
           is in check at the passed in square
        """
        king_square = self.board.king(self.board.turn)
        if square == king_square and self.board.is_check():
            return True
        return False

    @staticmethod
    def is_light_square(square: chess.Square) -> bool:
        """Returns True if the square passed in is a light square"""
        if square in chess.SQUARES:
            return chess.BB_LIGHT_SQUARES & chess.BB_SQUARES[square]
        else:
            raise(ValueError(f"Illegal square: {square}"))

    def is_white_orientation(self) -> bool:
        """Returns True if the board orientation is set as white"""
        return self.board_orientation is chess.WHITE

    def _notify_board_model_updated(self) -> None:
        """Notifies listeners of board model updates"""
        self.e_board_model_updated.notify()

    def _notify_successful_move_made(self) -> None:
        """Notifies listeners that a board move has been made"""
        self.e_successful_move_made.notify()

    def _log_init_info(self):
        """Logs class initialization"""
        log.debug("=============== BOARD INITIALIZATION ===============")
        log.debug(f"My color: {chess.COLOR_NAMES[self.my_color]}")
        log.debug(f"Variant: {self.get_variant_name()}")
        log.debug(f"Starting FEN: {self.board.fen()}")
        log.debug("====================================================")
