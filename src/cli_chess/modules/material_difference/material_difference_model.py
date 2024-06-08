from cli_chess.modules.board import BoardModel
from cli_chess.utils import EventManager
from typing import Dict
from chess import PIECE_SYMBOLS, PIECE_TYPES, PieceType, Color, COLORS, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
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

        self.material_difference: Dict[Color, Dict[PieceType, int]] = self.default_material_difference()
        self.score: Dict[Color, int] = self.default_score()

        self._event_manager = EventManager()
        self.e_material_difference_model_updated = self._event_manager.create_event()
        self.update()

    @staticmethod
    def default_material_difference() -> Dict[Color, Dict[PieceType, int]]:
        """Returns a default material difference dictionary"""
        return {
            WHITE: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0},
            BLACK: {KING: 0, QUEEN: 0, ROOK: 0, BISHOP: 0, KNIGHT: 0, PAWN: 0}
        }

    @staticmethod
    def default_score() -> Dict[Color, int]:
        """Returns a default score dictionary"""
        return {WHITE: 0, BLACK: 0}

    @staticmethod
    def generate_pieces_fen(board_fen: str) -> str:
        """Generates a fen containing pieces only by
           parsing the passed in board fen
           Example: rnbqkbnrppppppppPPPPPPPPRNBQKBNR"""
        pieces_fen = ""
        if board_fen:
            regex = re.compile('[^a-zA-Z]')
            pieces_fen = regex.sub('', board_fen)
        return pieces_fen

    def _reset_all(self) -> None:
        """Reset variables to default state"""
        self.material_difference = self.default_material_difference()
        self.score = self.default_score()

    def update(self, *args, **kwargs) -> None: # noqa
        """Update the material difference using the latest board FEN"""
        variant = self.board_model.get_variant_name()

        if variant != "horde":
            self._reset_all()

            if variant == "crazyhouse":  # Show material difference in pocket format
                self._update_material_difference_crazyhouse(variant)
            else:
                pieces_fen = self.generate_pieces_fen(self.board_model.board.board_fen())

                # Todo: Update to use chess.Piece()?
                for piece in pieces_fen:
                    color = WHITE if piece.isupper() else BLACK
                    piece_type = PIECE_SYMBOLS.index(piece.lower())

                    self._update_material_difference(color, piece_type)
                    self._update_score(color, piece_type)

                if variant == "3check":
                    self.material_difference[WHITE][KING] = 3 - self.board_model.board.remaining_checks[WHITE]
                    self.material_difference[BLACK][KING] = 3 - self.board_model.board.remaining_checks[BLACK]

            self._notify_material_difference_model_updated()

    def _update_material_difference(self, color: Color, piece_type: PieceType) -> None:
        """Updates the material difference based on the passed in piece"""
        if piece_type in PIECE_TYPES:
            opponent_piece_type_count = self.material_difference[not color][piece_type]

            if opponent_piece_type_count > 0:
                self.material_difference[not color][piece_type] -= 1
            else:
                self.material_difference[color][piece_type] += 1

    def _update_material_difference_crazyhouse(self, variant: str) -> None:
        """Updates the material difference to represent the crazyhouse pocket data.
           This function should only ever be called on confirmed crazyhouse games.
        """
        if variant == "crazyhouse":
            for color in COLORS:
                for _, piece in enumerate(str(self.board_model.board.pockets[color])):
                    piece_type = PIECE_SYMBOLS.index(piece.lower())
                    self.material_difference[color][piece_type] += 1

    def _update_score(self, color: Color, piece_type: PieceType) -> None:
        """Uses the material difference to
           calculate the score for each side"""
        if piece_type in PIECE_TYPES:
            self.score[color] += PIECE_VALUE[piece_type]

            advantage_color = WHITE if self.score[WHITE] > self.score[BLACK] else BLACK
            difference = abs(self.score[WHITE] - self.score[BLACK])
            self.score[advantage_color] = difference
            self.score[not advantage_color] = 0

    def get_material_difference(self, color: Color) -> Dict[PieceType, int]:
        """Returns the material difference dictionary associated to the passed in color"""
        return self.material_difference[color]

    def get_score(self, color: Color) -> int:
        """Returns the material difference
           score for the passed in color"""
        return self.score[color]

    def get_board_orientation(self) -> Color:
        """Returns the orientation of the board"""
        return self.board_model.get_board_orientation()

    def _notify_material_difference_model_updated(self) -> None:
        """Notifies listeners of material difference model updates"""
        self.e_material_difference_model_updated.notify()

    def cleanup(self) -> None:
        """Handles model cleanup tasks. This should only ever
           be run when this model is no longer needed.
        """
        self._event_manager.purge_all_events()
