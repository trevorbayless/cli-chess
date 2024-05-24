# Copyright (C) 2021-2024 Trevor Bayless <trevorbayless1@gmail.com>
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

from __future__ import annotations
from cli_chess.core.game import PlayableGameViewBase
from prompt_toolkit.layout import Container, HSplit, VSplit, VerticalAlign
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game.online_game import OnlineGamePresenter


class OnlineGameView(PlayableGameViewBase):
    def __init__(self, presenter: OnlineGamePresenter):
        self.presenter = presenter
        super().__init__(presenter)

    def _create_container(self) -> Container:
        main_content = Box(
            HSplit([
                VSplit([
                    self.board_output_container,
                    HSplit([
                        self.clock_upper,
                        self.player_info_upper_container,
                        self.material_diff_upper_container,
                        self.move_list_container,
                        self.material_diff_lower_container,
                        self.player_info_lower_container,
                        self.clock_lower
                    ])
                ]),
                self.input_field_container,
                self.premove_container,
                self.alert,
            ]),
            padding=0
        )
        function_bar = HSplit([
            self._create_function_bar()
        ], align=VerticalAlign.BOTTOM)

        return HSplit([main_content, function_bar], key_bindings=self.get_key_bindings())
