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
from random import getrandbits, randint
from typing import List
import chess.variant
import chess


class BoardModel:
    def __init__(self, game_parameters: dict, fen: str = "") -> None:
        self.game_parameters = game_parameters
        self.my_color: chess.Color = self._set_my_color(self.game_parameters['color'])
        self.board_orientation = self.my_color
        self.variant = self.game_parameters['variant']
        self.is_chess960 = self.variant == "chess960"

        if not self.is_chess960:
            if fen:
                self.board = chess.variant.find_variant(self.variant)(fen)
            else:
                self.board = chess.variant.find_variant(self.variant)()

        else:
            if fen:
                self.board = chess.Board(fen, chess960=True)
            else:
                # Todo: allow setting custom chess960 position by supplying a custom starting pos int
                self.board = chess.Board.from_chess960_pos(randint(0, 959))

        self._log_initialization()
        self.e_board_model_updated = Event()

    def _board_model_updated(self) -> None:
        """Notifies listeners of board model updates"""
        self.e_board_model_updated.notify()

    def make_move(self, move: str, human=True) -> None:
        """Attempts to make a move on the board.
           Raises a ValueError on illegal moves.
        """
        player = "human" if human else "engine"
        try:
            self.board.push_san(move)
            self._board_model_updated()
            log.info(f"make_move ({player}): {move}")
        except Exception as e:
            log.info(f"make_move ({player}): {e}")
            raise e

    def get_move_stack(self) -> List[chess.Move]:
        """Returns the boards move stack"""
        return self.board.move_stack

    def get_variant_name(self) -> str:
        """Returns a string holding the board variant name"""
        return self.board.uci_variant

    def _set_my_color(self, color: str) -> chess.Color:
        """Sets the color to play as based on the color string passed in"""
        if color.lower() in chess.COLOR_NAMES:
            return chess.Color(chess.COLOR_NAMES.index(color))
        else:  # Get random color to play as
            return chess.Color(getrandbits(1))

    def get_turn(self) -> chess.Color:
        """Returns the color of which turn it is"""
        return self.board.turn

    def get_board_orientation(self) -> chess.Color:
        """Returns the board orientation"""
        return self.board_orientation

    def set_board_orientation(self, color: chess.Color) -> None:
        """Sets the board's orientation to the color passed in"""
        self.board_orientation = color
        log.debug(f"board orientation set (orientation = {color}")

    def get_board_squares(self) -> list:
        """Returns the boards square numbers as a list based current board orientation"""
        square_numbers = []
        square_names = []

        for rank in range(len(chess.RANK_NAMES)-1, -1, -1):
            for file in range(len(chess.FILE_NAMES)):
                square_index = chess.square(file, rank)
                square_names.append(chess.square_name(square_index))
                square_numbers.append(chess.square(file, rank))

        if self.board_orientation is chess.BLACK:
            return square_numbers[::-1]

        return square_numbers

    def get_square_file_index(self, square: chess.Square) -> int:
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

    def get_square_rank_index(self, square: chess.Square) -> int:
        """Returns the rank index of the passed in square"""
        return chess.square_rank(square)

    def get_rank_label(self, rank_index: int) -> str:
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

    def is_light_square(self, square: chess.Square) -> bool:
        """Returns True if the square passed in is a light square"""
        if square in chess.SQUARES:
            return chess.BB_LIGHT_SQUARES & chess.BB_SQUARES[square]
        else:
            raise(ValueError(f"Illegal square: {square}"))

    def is_white_orientation(self) -> bool:
        """Returns True if the board orientation is set as white"""
        if self.board_orientation is chess.WHITE:
            return True
        else:
            return False

    def _log_initialization(self):
        """Logs class initialization"""
        log.debug("=============== BOARD INITIALIZATION ===============")
        log.debug(f"Game parameters: {self.game_parameters}")
        log.debug(f"Color: {chess.COLOR_NAMES[self.my_color]}")
        log.debug(f"Starting FEN: {self.board.fen()}")
        log.debug(f"Variant: {self.variant}")
        log.debug("====================================================")
