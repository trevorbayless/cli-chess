# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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


class BoardModel:
    def __init__(self, orientation: chess.Color = chess.WHITE, variant="standard", fen="") -> None:
        self.board = self._initialize_board(variant, fen)
        self.initial_fen = self.board.fen()
        self.my_color = orientation
        self.orientation = chess.WHITE if variant.lower() == "racingkings" else orientation

        self._log_init_info()
        self.e_board_model_updated = Event()
        self.e_successful_move_made = Event()

    @staticmethod
    def _initialize_board(variant: str, fen: str):
        """Initializes the main board object"""
        if fen == "startpos":
            fen = ""

        if variant == "chess960":
            if fen:
                return chess.Board(fen, chess960=True)
            else:
                return chess.Board.from_chess960_pos(randint(0, 959))
        else:
            if fen:
                return chess.variant.find_variant(variant)(fen)
            return chess.variant.find_variant(variant)()

    def reinitialize_board(self, variant: str, orientation: chess.Color, fen: str = ""):
        """Reinitializes the existing board object to the new variant/fen"""
        try:
            self.board = self._initialize_board(variant, fen)
            self.initial_fen = self.board.fen()
            self.my_color = orientation
            self.orientation = chess.WHITE if variant.lower() == "racingkings" else orientation
            self.e_board_model_updated.notify()
        except ValueError as e:
            log.error(f"Error while trying to reinitialize the board: {e}")
            raise

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

    def make_moves_from_list(self, move_list: list) -> None:
        """Attempts to make all moves in the provided move list.
           Raises a ValueError on an illegal move.
        """
        for move in move_list:
            try:
                self.board.push_san(move)
            except ValueError as e:
                log.error(f"Invalid move while making moves from list: {e}")

        self._notify_board_model_updated()

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
        return self.orientation

    def set_board_orientation(self, color: chess.Color, notify=True) -> None:
        """Sets the board's orientation to the color passed in.
           If notify is false, a model update notification will not be sent.
        """
        self.orientation = color
        log.debug(f"board orientation set (orientation = {color})")

        if notify:
            self._notify_board_model_updated()

    def set_fen(self, fen: str, notify=True) -> None:
        """Sets the board FEN. Raises ValueError if syntactically invalid.
           If notify is false, a model update notification will not be sent.
        """
        try:
            self.board.set_fen(fen)
            self.initial_fen = fen

            if notify:
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

        if self.orientation is chess.BLACK:
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
        if self.orientation is chess.BLACK:
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
        return self.orientation is chess.WHITE

    def set_board_position(self, fen: str, orientation: chess.Color = None, uci_last_move=""):
        """Sets up the board using the passed in FEN. In addition, optionally the
           board orientation and last move can also be passed in. The last move must be
           passed in using the UCI format. Passing in the last move is only for handling
           board highlights with a FEN. It does not affect the move stack.
        """
        try:
            if fen:
                self.set_fen(fen, notify=False)
                highlight_move = chess.Move.from_uci(uci_last_move) if uci_last_move else chess.Move.null()
                if isinstance(orientation, bool):
                    self.set_board_orientation(orientation, notify=False)

                if bool(highlight_move):
                    self.e_board_model_updated.notify(force_highlight_move=highlight_move)
                else:
                    self.e_board_model_updated.notify()
        except Exception as e:
            log.error(f"Error caught setting board position: {e}")

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
