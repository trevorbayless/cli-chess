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
from cli_chess.menus import MultiValueMenuView
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.vs_computer_menu.vs_computer_menu_presenter import VsComputerMenuPresenter


class VsComputerMenuView(MultiValueMenuView):
    def __init__(self, presenter: VsComputerMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=40, column_width=22)

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.handle_start_game)),
            ("class:function-bar.label", f"{'Start game':<14}", handle_mouse_click(self.presenter.handle_start_game)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Creates the key bindings associated to the function bar fragments"""
        kb = KeyBindings()
        kb.add(Keys.F1)(handle_bound_key_pressed(self.presenter.handle_start_game))
        return kb
