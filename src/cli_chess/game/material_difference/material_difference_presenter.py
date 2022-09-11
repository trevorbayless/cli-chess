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

from . import MaterialDifferenceModel, MaterialDifferenceView
from cli_chess.game.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
from chess import Color, PIECE_TYPES, PIECE_SYMBOLS


class MaterialDifferencePresenter:
    def __init__(self, material_diff_model: MaterialDifferenceModel):
        self.material_diff_model = material_diff_model

        self.is_proper_variant = self.material_diff_model.board_model.game_parameters['variant'] != "horde"

        self.view_upper = MaterialDifferenceView(self, self.format_diff_output(not self.material_diff_model.board_orientation), self.is_proper_variant)
        self.view_lower = MaterialDifferenceView(self, self.format_diff_output(self.material_diff_model.board_orientation), self.is_proper_variant)

        self.material_diff_model.e_material_difference_model_updated.add_listener(self.update)

    def update(self) -> None:
        """Updates the material differences for both sides"""
        self.view_upper.update(self.format_diff_output(not self.material_diff_model.board_orientation))
        self.view_lower.update(self.format_diff_output(self.material_diff_model.board_orientation))

    def format_diff_output(self, color: Color) -> str:
        """Returns the formatted difference of the color passed in as a string"""
        output = ""
        material_difference = self.material_diff_model.get_material_difference(color)
        score = self.material_diff_model.get_score(color)
        use_unicode = board_config.get_boolean(board_config.Keys.USE_UNICODE_PIECES)

        for piece_type in PIECE_TYPES:
            for count in range(material_difference[piece_type]):
                if use_unicode:
                    output += get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type])
                else:
                    output += PIECE_SYMBOLS[piece_type].upper()

        if score > 0:
            output += f"+{score}"

        return output
