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
from cli_chess.core.game import GameViewBase
from prompt_toolkit.layout import Container, Window, VSplit, HSplit, VerticalAlign, D
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game.online_game.watch_tv import WatchTVPresenter


class WatchTVView(GameViewBase):
    def __init__(self, presenter: WatchTVPresenter):
        self.presenter = presenter
        self.move_list_placeholder = Window(always_hide_cursor=True)
        super().__init__(presenter)

    def _create_container(self) -> Container:
        """Creates the container for the TV view"""
        main_content = Box(
            HSplit([
                VSplit([
                    self.board_output_container,
                    HSplit([
                        self.clock_upper,
                        self.player_info_upper_container,
                        self.material_diff_upper_container,
                        Box(self.move_list_placeholder, height=D(min=1, max=4)),
                        self.material_diff_lower_container,
                        self.player_info_lower_container,
                        self.clock_lower
                    ]),
                ]),
                self.alert
            ]),
            padding=0
        )
        function_bar = HSplit([
            self._create_function_bar()
        ], align=VerticalAlign.BOTTOM)

        return HSplit([main_content, function_bar], key_bindings=self.get_key_bindings())
