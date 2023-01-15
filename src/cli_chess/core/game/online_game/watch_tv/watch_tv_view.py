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
from cli_chess.modules.board import BoardView
from cli_chess.modules.material_difference import MaterialDifferenceView
from cli_chess.utils.ui_common import handle_mouse_click, go_back_to_main_menu
from prompt_toolkit.layout import Container, Window, FormattedTextControl, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
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
            HSplit([
                self._create_function_bar()
            ], align=VerticalAlign.BOTTOM)
        ], key_bindings=self._container_key_bindings())

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            return ([
                ("class:function_bar.key", "F10", handle_mouse_click(self.presenter.go_back)),
                ("class:function_bar.label", f"{'Main menu':<14}", handle_mouse_click(self.presenter.go_back))
            ])

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
        ], height=D(max=1, preferred=1))

    def _container_key_bindings(self) -> KeyBindings:
        """Creates the key bindings for this container"""
        bindings = KeyBindings()

        @bindings.add(Keys.F10, eager=True)
        def _(event): # noqa
            self.presenter.go_back()

        return bindings

    @staticmethod
    def exit_view() -> None:
        """Exits this view and returns to the main menu"""
        go_back_to_main_menu()

    def __pt_container__(self) -> Container:
        """Return the watch tv container"""
        return self.root_container
