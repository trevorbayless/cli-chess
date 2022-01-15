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

from cli_chess.game.board import BoardModel
from cli_chess.utils import Event
from typing import Dict
from chess import (PIECE_SYMBOLS, PIECE_TYPES, PieceType, Color, WHITE, BLACK,
                   PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
import re

PIECE_VALUE: Dict[PieceType, int] = {
    KING: 0,
    QUEEN: 9,
    ROOK: 5,
    BISHOP: 3,
    KNIGHT: 3,
    PAWN: 1,
}


class MaterialDifferenceModel:
    def __init__(self, board_model: BoardModel):
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)

        self.piece_count: Dict[Color, Dict[PieceType, int]] = self.empty_count()
        self.material_difference: Dict[Color, Dict[PieceType, int]] = self.empty_count()
        self.score: Dict[Color, int] = self.empty_score()

        self.e_material_difference_model_updated = Event()
        self.update()

    def _material_difference_model_updated(self) -> None:
        """Notifies listeners of material difference model updates"""
        self.e_material_difference_model_updated.notify()

    def empty_count(self) -> Dict[Color, Dict[PieceType, int]]:
        """Returns an empty piece count dictionary"""
        return {
            WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0},
            BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
        }

    def empty_score(self) -> Dict[Color, int]:
        """Returns an empty score dictionary"""
        return {WHITE: 0, BLACK: 0}

    def reset_all(self) -> None:
        """Reset variables to default state"""
        self.piece_count = self.empty_count()
        self.material_difference = self.empty_count()
        self.score = self.empty_score()

    def update(self) -> None:
        """Update the material difference using the latest board FEN"""
        self.reset_all()
        pieces_fen = self.generate_pieces_fen(self.board_model.board.board_fen())

        for piece in pieces_fen:
            color = WHITE if piece.isupper() else BLACK
            piece_type = PIECE_SYMBOLS.index(piece.lower())
            self.tally_piece(color, piece_type)
            self.update_material_difference(color, piece_type)
            self.update_score(color, piece_type)

        self._material_difference_model_updated()

    def generate_pieces_fen(self, board_fen: str) -> str:
        """Generates a fen containing pieces only by
           parsing the passed in board fen
           Example: rnbqkbnrppppppppPPPPPPPPRNBQKBNR"""
        pieces_fen = ""
        if board_fen:
            regex = re.compile('[^a-zA-Z]')
            pieces_fen = regex.sub('', board_fen)
        return pieces_fen

    def tally_piece(self, color: Color, piece_type: PieceType) -> None:
        """Tallies and updates the piece count
           based on the passed in piece"""
        if piece_type in PIECE_TYPES:
            self.piece_count[color][piece_type] += 1

    def update_material_difference(self, color: Color, piece_type: PieceType) -> None:
        """Updates the material difference based on the passed in piece"""
        if piece_type in PIECE_TYPES:
            piece_type_count = self.material_difference[not color][piece_type]
            if piece_type_count > 0:
                self.material_difference[not color][piece_type] -= 1
            else:
                self.material_difference[color][piece_type] += 1

    def update_score(self, color: Color, piece_type: PieceType) -> None:
        """Uses the material difference to
           calculate the score for each side"""
        if piece_type in PIECE_TYPES:
            piece_value = PIECE_VALUE[piece_type]
            self.score[color] += piece_value

            color_ahead = WHITE if self.score[WHITE] > self.score[BLACK] else BLACK
            difference = abs(self.score[WHITE] - self.score[BLACK])
            self.score[color_ahead] = difference
            self.score[not color_ahead] = 0

    def get_material_difference(self, color: Color) -> Dict[PieceType, int]:
        """Returns the material difference dictionary for passed in color"""
        return self.material_difference[color]

    def get_score(self, color: Color) -> int:
        """Returns the material difference
           score for the passed in color"""
        return self.score[color]
