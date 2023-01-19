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
from cli_chess.__metadata__ import __version__
from cli_chess.utils.ui_common import handle_mouse_click, exit_app
from prompt_toolkit.layout import Window, FormattedTextControl, ConditionalContainer, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import to_filter
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainPresenter


class MainView:
    def __init__(self, presenter: MainPresenter):
        self.presenter = presenter
        self._error_label = FormattedTextControl(text="", style="class:label.error.banner", show_cursor=False)
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the main view"""
        return HSplit([
            VSplit([
                Box(self.presenter.main_menu_presenter.view, padding=0, padding_right=1),
            ]),
            HSplit([
                self._create_error_container(),
                self._create_function_bar()
            ], align=VerticalAlign.BOTTOM)
        ], key_bindings=merge_key_bindings([self._container_key_bindings(), self._create_function_bar_key_bindings()]))

    def _create_error_container(self) -> ConditionalContainer:
        """Create the container used to display errors"""
        return ConditionalContainer(
            Window(self._error_label, always_hide_cursor=True, height=D(max=1)),
            filter=to_filter(self._error_label.text == "")
        )

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments = self.presenter.main_menu_presenter.view.get_function_bar_fragments()
            self._error_label.text = ""

            if fragments:
                fragments.append(("class:function-bar.spacer", " "))

            fragments.extend([
                ("class:function-bar.key", "F10", handle_mouse_click(exit_app)),
                ("class:function-bar.label", f"{'Quit':<14}", handle_mouse_click(exit_app))
            ])

            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
            Window(FormattedTextControl(f"cli-chess {__version__}"), align=WindowAlign.RIGHT)
        ], height=D(max=1, preferred=1))

    def _create_function_bar_key_bindings(self) -> "_MergedKeyBindings":
        """Creates the key bindings for the function bar"""
        main_menu_key_bindings = self.presenter.main_menu_presenter.view.get_function_bar_key_bindings()

        # Always included key bindings
        always_included_bindings = KeyBindings()
        always_included_bindings.add(Keys.F10)(exit_app)

        return merge_key_bindings([main_menu_key_bindings, always_included_bindings])

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

    def print_error(self, err: str) -> None:
        """Print the passed in error to the error container"""
        self._error_label.text = err

    def clear_error(self) -> None:
        """Clear any errors displayed in the error container"""
        self._error_label.text = ""

    def __pt_container__(self):
        return self._container
