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

from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.modules.board import BoardView
from cli_chess.modules.move_list import MoveListView
from cli_chess.modules.material_difference import MaterialDifferenceView
from prompt_toolkit.layout import Container, HSplit, VSplit
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game.online_game.watch_tv import WatchTVPresenter


# TODO: Update this (as well as the presenter) to utilize the GamePresenterBase and GameViewBase classes
class WatchTVView:
    def __init__(self, presenter: WatchTVPresenter, board_view: BoardView,
                 material_diff_upper_view: MaterialDifferenceView, material_diff_lower_view: MaterialDifferenceView) -> None:
        self.presenter = presenter
        self.board_output_container = board_view
        self.material_diff_upper_container = material_diff_upper_view
        self.material_diff_lower_container = material_diff_lower_view
        self.root_container = self._create_root_container()

    def _create_root_container(self) -> Container:
        return HSplit([
            VSplit([
                self.board_output_container,
                HSplit([
                    self.material_diff_upper_container,
                    self.material_diff_lower_container,
                ]),
            ]),
        ])

    def __pt_container__(self) -> Container:
        """Return the watch tv container"""
        return self.root_container
