from . import MaterialDifferenceModel, MaterialDifferenceView
from cli_chess.game.common import get_piece_unicode_symbol
from cli_chess.utils import config
from chess import Color, PIECE_TYPES, PIECE_SYMBOLS
from typing import Dict


class MaterialDifferencePresenter:
    def __init__(self, model: MaterialDifferenceModel, color: Color):
        self.model = model
        self.color = color
        self.model.e_material_difference_model_updated.add_listener(self.update_difference)
        self.view = MaterialDifferenceView(self)


    def format_output(self) -> str:
        """Returns the formatted difference as a string"""
        output = ""
        material_diff_data = self.model.get_material_difference(self.color)
        material_diff_score = self.model.get_score(self.color)
        use_unicode = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for piece_type in PIECE_TYPES:
            for count in range(material_diff_data[piece_type]):
                if use_unicode:
                    output += get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type])
                else:
                    output += PIECE_SYMBOLS[piece_type].upper()

        if material_diff_score > 0:
            output += f"+{material_diff_score}"

        return output


    def update_difference(self):
        """Updates the views output"""
        self.view.update(self.format_output())