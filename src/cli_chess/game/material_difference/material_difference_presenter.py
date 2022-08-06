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
from cli_chess.utils import config
from chess import Color, PIECE_TYPES, PIECE_SYMBOLS


class MaterialDifferencePresenter:
    def __init__(self, material_diff_model: MaterialDifferenceModel, color: Color):
        self.material_diff_model = material_diff_model
        self.color = color

        self.is_proper_variant = self.material_diff_model.board_model.game_parameters['variant'] != "horde"
        self.view = MaterialDifferenceView(self, self.format_diff_output(), self.is_proper_variant)

        self.material_diff_model.e_material_difference_model_updated.add_listener(self.update)

    def update(self) -> None:
        """Updates the material difference"""
        if self.is_proper_variant:
            self.view.update(self.format_diff_output())

    def format_diff_output(self) -> str:
        """Returns the formatted difference as a string"""
        output = ""
        material_difference = self.material_diff_model.get_material_difference(self.color)
        score = self.material_diff_model.get_score(self.color)
        use_unicode = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for piece_type in PIECE_TYPES:
            for count in range(material_difference[piece_type]):
                if use_unicode:
                    output += get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type])
                else:
                    output += PIECE_SYMBOLS[piece_type].upper()

        if score > 0:
            output += f"+{score}"

        return output
