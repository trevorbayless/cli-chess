from __future__ import annotations
from cli_chess.modules.material_difference import MaterialDifferenceView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import game_config
from chess import Color, PIECE_TYPES, PIECE_SYMBOLS, KING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.material_difference import MaterialDifferenceModel


class MaterialDifferencePresenter:
    def __init__(self, model: MaterialDifferenceModel):
        self.model = model
        self.show_diff = self.model.board_model.get_variant_name() != "horde"
        self.is_crazyhouse = self.model.board_model.get_variant_name() == "crazyhouse"

        orientation = self.model.get_board_orientation()
        self.view_upper = MaterialDifferenceView(self, self.format_diff_output(not orientation), self.show_diff)
        self.view_lower = MaterialDifferenceView(self, self.format_diff_output(orientation), self.show_diff)

        self.model.e_material_difference_model_updated.add_listener(self.update)
        game_config.e_game_config_updated.add_listener(self.update)

    def update(self) -> None:
        """Updates the material differences for both sides"""
        orientation = self.model.get_board_orientation()
        self.view_upper.update(self.format_diff_output(not orientation))
        self.view_lower.update(self.format_diff_output(orientation))

    def format_diff_output(self, color: Color) -> str:
        """Returns the formatted difference of the color passed in as a string"""
        output = ""
        material_difference = self.model.get_material_difference(color)
        use_unicode = game_config.get_boolean(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE)
        pad_unicode = game_config.get_boolean(game_config.Keys.PAD_UNICODE)

        if self.is_crazyhouse:
            return self._get_crazyhouse_pocket_output(color, use_unicode, pad_unicode)

        for piece_type in PIECE_TYPES:
            for count in range(material_difference[piece_type]):
                symbol = get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type]) if use_unicode else PIECE_SYMBOLS[piece_type].upper()

                if symbol and use_unicode and pad_unicode:
                    # Pad unicode symbol with a space (if pad_unicode is true) to help unicode/ascii character overlap
                    symbol = symbol + " "

                output = symbol + output if piece_type != KING else output + symbol  # Add king to end for 3check

        score = self.model.get_score(color)
        if score > 0:
            output += f"+{score}"

        return output

    def _get_crazyhouse_pocket_output(self, color: Color, use_unicode: bool, pad_unicode: bool) -> str:
        """Returns the formatted crazyhouse pocket for the color passed in as a string"""
        output = ""
        material_difference = self.model.get_material_difference(color)

        for piece_type in PIECE_TYPES:
            if piece_type == KING:
                continue

            piece_count = material_difference[piece_type]
            if piece_count > 0:
                symbol = get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type]) if use_unicode else PIECE_SYMBOLS[piece_type].upper()

                if symbol and use_unicode and pad_unicode:
                    # Pad unicode symbol with a space (if pad_unicode is true) to help unicode/ascii character overlap
                    symbol = symbol + " "

                output = output + symbol + f"({piece_count}) "

        return output
