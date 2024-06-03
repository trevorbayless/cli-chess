from __future__ import annotations
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.layout import Window, ConditionalContainer, VSplit, HSplit, D
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
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
        self._token_input = self._create_token_input_area()
        self._container = self._create_container()

    def _create_token_input_area(self):
        """Creates and returns the TextArea used for token input"""
        validator = Validator.from_callable(
            self.presenter.update_linked_account,
            error_message="Invalid token or missing scopes",
            move_cursor_to_end=True,
        )

        return TextArea(
            validator=validator,
            accept_handler=lambda x: True,
            style="class:text-area.input",
            focus_on_click=True,
            wrap_lines=True,
            multiline=False,
            width=D(max=self.container_width),
            height=D(max=1),
        )

    def _create_container(self) -> HSplit:
        """Creates the container for the token manager view"""
        return HSplit([
            Label(f"{'Authenticate with Lichess':<{self.container_width}}", style="class:menu.category-title", wrap_lines=False),
            VSplit([
                Label("API Token: ", style="bold", dont_extend_width=True),
                ConditionalContainer(
                    TextArea("Input token and press enter", style="class:text-area.input.placeholder", focus_on_click=True),
                    filter=Condition(lambda: not self.has_focus()) & Condition(lambda: len(self._token_input.text) == 0)
                ),
                ConditionalContainer(self._token_input, Condition(lambda: self.has_focus()) | Condition(lambda: len(self._token_input.text) > 0)),
            ], height=D(max=1)),
            ValidationToolbar(),
            Box(Window(), height=D(max=1)),
            VSplit([
                Label("Linked account: ", dont_extend_width=True),
                ConditionalContainer(Label("None", style="class:label.error bold italic"), Condition(lambda: not self.lichess_username)),
                ConditionalContainer(Label(text=lambda: self.lichess_username, style="class:label.success bold"), Condition(lambda: self.lichess_username != "")),  # noqa: E501
            ], height=D(max=1)),
        ], width=D(max=self.container_width), height=D(preferred=8))

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns a set of function bar fragments to use if
           this module is hooked up with a function bar
        """
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.open_token_creation_url)),
            ("class:function-bar.label", f"{'Open token creation URL':<25}", handle_mouse_click(self.presenter.open_token_creation_url)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Returns a set of key bindings to use if this
           module is hooked up with a function bar
        """
        kb = KeyBindings()
        kb.add(Keys.F1)(handle_bound_key_pressed(self.presenter.open_token_creation_url))
        return kb

    def has_focus(self):
        """Returns true if this container has focus"""
        has_focus = get_app().layout.has_focus(self._container)
        if has_focus:
            get_app().layout.focus(self._token_input)
        return has_focus

    def __pt_container__(self) -> HSplit:
        return self._container
