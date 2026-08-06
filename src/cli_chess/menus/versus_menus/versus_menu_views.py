from __future__ import annotations
from cli_chess.menus import MultiValueMenuView
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.layout import Container, VSplit, HSplit, D
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import Label, TextArea, ValidationToolbar
from prompt_toolkit.validation import Validator
from prompt_toolkit.application import get_app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.versus_menus.versus_menu_presenters import VersusMenuPresenter, OnlineVsPlayerMenuPresenter


class VersusMenuView(MultiValueMenuView):
    def __init__(self, presenter: VersusMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=38, column_width=18)

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


class OnlineVsPlayerMenuView(VersusMenuView):
    def __init__(self, presenter: OnlineVsPlayerMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter)

    def _create_container(self) -> Container:
        """Creates the container for the challenge a player menu"""
        self._username_input = self._create_username_input_area()
        self._menu_container = super()._create_container()
        return HSplit([
            VSplit([
                Label("Opponent: ", style="bold", dont_extend_width=True),
                self._username_input,
            ], height=D(min=1, max=1), key_bindings=self._create_username_key_bindings()),
            ValidationToolbar(),
            self._menu_container,
        ])

    def _create_username_input_area(self) -> TextArea:
        """Creates and returns the TextArea used for the opponents username input"""
        validator = Validator.from_callable(
            self.presenter.validate_username,
            error_message="User not found on Lichess",
            move_cursor_to_end=True,
        )

        return TextArea(
            validator=validator,
            accept_handler=lambda x: True,
            style="class:text-area.input",
            focus_on_click=True,
            multiline=False,
            width=D(max=self.container_width),
            height=D(max=1),
        )

    def _create_username_key_bindings(self) -> KeyBindings:
        """Creates the key bindings associated to the username input"""
        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        @bindings.add(Keys.Down)
        def _(event): # noqa
            """Move focus to the menu options"""
            self.focus()

        return bindings

    def get_username(self) -> str:
        """Returns the username of the player to challenge"""
        return self._username_input.text.strip()

    def has_focus(self) -> bool:
        """Returns true if the menu options have focus"""
        return get_app().layout.has_focus(self._menu_container)

    def focus(self) -> None:
        """Focus on the menu options"""
        get_app().layout.focus(self._menu_container)

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.handle_start_game)),
            ("class:function-bar.label", f"{'Send challenge':<14}", handle_mouse_click(self.presenter.handle_start_game)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Creates the key bindings associated to the function bar fragments"""
        kb = KeyBindings()
        kb.add(Keys.F1)(handle_bound_key_pressed(self.presenter.handle_start_game))
        return kb
