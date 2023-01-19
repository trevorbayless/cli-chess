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
from prompt_toolkit.layout import Window, ConditionalContainer, VSplit, HSplit, D
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import Label, Box, TextArea, ValidationToolbar
from prompt_toolkit.validation import Validator
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.token_manager import TokenManagerPresenter


class TokenManagerView:
    def __init__(self, presenter: TokenManagerPresenter):
        self.presenter = presenter
        self.container_width = 40
        self.lichess_username = ""
        self._text_input = self._create_text_input_area()
        self._container = self._create_container()

    def _create_text_input_area(self):
        """Creates and returns the TextArea used for token input"""
        validator = Validator.from_callable(
            self.presenter.update_linked_account,
            error_message="Invalid Lichess API token",
            move_cursor_to_end=True,
        )

        return TextArea(
            validator=validator,
            accept_handler=lambda x: True,
            focus_on_click=True,
            wrap_lines=True,
            multiline=False,
            width=D(max=self.container_width),
            height=D(max=1),
        )

    def _create_container(self) -> HSplit:
        """Creates the container for the token manager view"""
        return HSplit([
            Label(f"{'Authenticate with Lichess':<{self.container_width}}", style="class:menu.category_title", wrap_lines=False),
            VSplit([
                Label("API Token: ", style="bold", dont_extend_width=True),
                ConditionalContainer(
                    TextArea("Input token and press enter", style="class:text-area-placeholder", focus_on_click=True),
                    filter=Condition(lambda: not self.has_focus()) & Condition(lambda: len(self._text_input.text) == 0)
                ),
                ConditionalContainer(self._text_input, Condition(lambda: self.has_focus()) | Condition(lambda: len(self._text_input.text) > 0)),
            ], height=D(max=1)),
            ValidationToolbar(),
            Box(Window(), height=D(max=1)),
            VSplit([
                Label("Linked account: ", dont_extend_width=True),
                ConditionalContainer(Label("None", style="class:label.error bold italic"), Condition(lambda: not self.lichess_username)),
                ConditionalContainer(Label(text=lambda: self.lichess_username, style="class:label.success bold"), Condition(lambda: self.lichess_username != "")),
            ], height=D(max=1)),
        ], width=D(max=self.container_width), height=D(preferred=8))

    @staticmethod
    def get_function_bar_fragments() -> StyleAndTextTuples:
        """Returns a set of function bar fragments to use if
           this module is hooked up with a function bar
        """
        fragments: StyleAndTextTuples = []
        return fragments

    def get_function_bar_key_bindings(self) -> ConditionalKeyBindings:
        """Returns a set of key bindings to use if this
           module is hooked up with a function bar
        """
        kb = KeyBindings()
        kb = ConditionalKeyBindings(
            kb,
            filter=Condition(lambda: self.has_focus())
        )
        return kb

    def has_focus(self):
        """Returns true if this container has focus"""
        has_focus = get_app().layout.has_focus(self._container)
        if has_focus:
            get_app().layout.focus(self._text_input)
        return has_focus

    def __pt_container__(self) -> HSplit:
        return self._container
