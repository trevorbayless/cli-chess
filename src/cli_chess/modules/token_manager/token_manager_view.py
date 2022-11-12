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
from cli_chess.utils import is_valid_lichess_token
from cli_chess.utils.ui_common import handle_mouse_click
from prompt_toolkit.layout import Window, FormattedTextControl, ConditionalContainer, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import TextArea, ValidationToolbar, Frame
from prompt_toolkit.validation import Validator
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.token_manager import TokenManagerPresenter

api_token_validator = Validator.from_callable(
    is_valid_lichess_token,
    error_message="Invalid Lichess API token",
    move_cursor_to_end=True,
)


class TokenManagerView:
    def __init__(self, presenter: TokenManagerPresenter):
        self.presenter = presenter
        self.container_width = 40
        self._text_input = self._create_text_input_area()
        self._container = self._create_container()

    def _create_text_input_area(self):
        """Creates and returns the TextArea used for token input"""
        return TextArea(
            prompt="Token: ",
            validator=api_token_validator,
            accept_handler=self._accept_handler,
            focus_on_click=True,
            wrap_lines=False,
            multiline=False,
            height=D(max=1)
        )

    def _create_container(self) -> HSplit:
        """Creates the container for the token manager view"""
        return HSplit([
            Window(
                FormattedTextControl(
                    text=f"{'Manage API Access Token':<{self.container_width}}",
                    style="class:menu.category_title"
                ),
                width=D(max=self.container_width),
                height=D(max=1),
            ),
            Window(FormattedTextControl("Enter your API token"), height=D(max=1)),
            self._text_input,
            ValidationToolbar(),
        ])

    def _accept_handler(self, buf) -> bool:
        """Called on ENTER after successful token validation.
           Saves the valid token to the configuration file.
        """
        self.presenter.save_api_token(self._text_input.text)
        return True

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns a set of function bar fragments to use if
           this module is hooked up with a function bar
        """
        fragments: StyleAndTextTuples = []
        if self.has_focus():
            @handle_mouse_click
            def handle_browser_open() -> None:
                self.presenter.open_token_creation_url()

            fragments.extend([
                ("class:function_bar.key", "F1", handle_browser_open),
                ("class:function_bar.label", f"{'Open browser':<14}", handle_browser_open),
            ])
        return fragments

    def get_function_bar_key_bindings(self):
        """Returns a set of key bindings to use if this
           module is hooked up with a function bar
        """
        kb = KeyBindings()

        @kb.add(Keys.F1)
        def _(event):
            self.presenter.open_token_creation_url()

        kb = ConditionalKeyBindings(
            kb,
            filter=Condition(lambda: self.has_focus())
        )
        return kb

    def has_focus(self):
        """Returns true if this container has focus"""
        return get_app().layout.has_focus(self._container)

    def __pt_container__(self) -> HSplit:
        return self._container
