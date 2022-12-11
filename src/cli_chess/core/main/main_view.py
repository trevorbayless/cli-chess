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

from __future__ import annotations
from cli_chess.__metadata__ import __version__
from cli_chess.utils.ui_common import handle_mouse_click, exit_app
from prompt_toolkit.layout import Window, FormattedTextControl, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import get_app
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainPresenter


class MainView:
    def __init__(self, presenter: MainPresenter):
        self.presenter = presenter
        self._function_bar_container = self._create_function_bar()
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the menu"""
        return HSplit([
            VSplit([
                Box(self.presenter.main_menu_presenter.view, padding=0, padding_right=1),
            ]),
            HSplit([
                self._function_bar_container
            ], align=VerticalAlign.BOTTOM)
        ], key_bindings=merge_key_bindings([self._container_key_bindings(), self._create_function_bar_key_bindings()]))

    @staticmethod
    def _create_function_bar() -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments: StyleAndTextTuples = []

            ##
            # Always included fragments
            ##
            @handle_mouse_click
            def handle_quit() -> None:
                get_app().exit()

            if fragments:
                fragments.append(("class:function_bar.spacer", " "))

            fragments.extend([
                ("class:function_bar.key", "F10", handle_quit),
                ("class:function_bar.label", f"{'Quit':<14}", handle_quit)
            ])

            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
            Window(FormattedTextControl(f"cli-chess {__version__}"), align=WindowAlign.RIGHT)
        ], height=D(max=1))

    @staticmethod
    def _create_function_bar_key_bindings() -> KeyBindings:
        """Creates the key bindings for the function bar"""
        kb = KeyBindings()
        kb.add(Keys.F10)(exit_app)
        return kb

    @staticmethod
    def _container_key_bindings() -> KeyBindings:
        """Creates the key bindings for this container"""
        bindings = KeyBindings()
        bindings.add(Keys.Right)(focus_next)
        bindings.add(Keys.ControlF)(focus_next)
        bindings.add(Keys.Tab)(focus_next)
        bindings.add(Keys.Left)(focus_previous)
        bindings.add(Keys.ControlB)(focus_previous)
        bindings.add(Keys.BackTab)(focus_previous)

        return bindings

    def __pt_container__(self):
        return self._container
