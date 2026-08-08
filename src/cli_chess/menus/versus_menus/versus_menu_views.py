from __future__ import annotations
from cli_chess.menus import MultiValueMenuView
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, HSplit, D, Window, FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import Label, TextArea, ValidationToolbar, Box
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
            self._menu_container,
            Box(Window(), height=D(min=1, max=1)),
            VSplit([
                Label("Opponent: ", style="bold", dont_extend_width=True),
                ConditionalContainer(
                    Window(FormattedTextControl(self._get_username_placeholder_fragments), style="class:text-area.input.placeholder"),
                    filter=Condition(lambda: not self._username_input_has_focus()) & Condition(lambda: len(self._username_input.text) == 0)
                ),
                ConditionalContainer(self._username_input, Condition(lambda: self._username_input_has_focus()) | Condition(lambda: len(self._username_input.text) > 0)),  # noqa: E501
            ], height=D(min=1, max=1), key_bindings=self._create_username_key_bindings()),
            ValidationToolbar(),
        ], width=D(max=self.container_width))

    def _create_username_input_area(self) -> TextArea:
        """Creates and returns the TextArea used for the opponents username input"""
        validator = Validator.from_callable(
            self.presenter.validate_username,
            error_message="User not found on Lichess",
            move_cursor_to_end=True,
        )

        return TextArea(
            validator=validator,
            accept_handler=self._accept_username,
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
        def _(event): # noqa
            """Move to the last menu option"""
            last_option = len(self.presenter.get_visible_menu_options()) - 1
            self.select_option(last_option)

        @bindings.add(Keys.Down)
        def _(event): # noqa
            """Move to the first menu option"""
            self.select_option(0)

        return bindings

    def _create_key_bindings(self) -> KeyBindings:
        """Create key bindings for menu navigation and input focus transitions"""
        bindings = super()._create_key_bindings()

        @bindings.add(Keys.Up, eager=True)
        def _(event): # noqa
            """Move to username input when pressing Up on the first menu option"""
            if self.selected_option <= 0:
                get_app().layout.focus(self._username_input)
                return

            self.select_previous_option()

        @bindings.add(Keys.Down, eager=True)
        def _(event): # noqa
            """Move to username input when pressing Down on the last menu option"""
            last_option = len(self.presenter.get_visible_menu_options()) - 1
            if self.selected_option >= last_option:
                get_app().layout.focus(self._username_input)
                return

            self.select_next_option()

        return bindings

    def get_username(self) -> str:
        """Returns the username of the player to challenge"""
        return self._username_input.text.strip()

    def _get_username_placeholder_fragments(self) -> StyleAndTextTuples:
        """Create clickable placeholder text that focuses the username input"""
        return [
            ("class:text-area.input.placeholder", "Enter opponent's username", handle_mouse_click(self.focus_username_input)),
        ]

    def _username_input_has_focus(self) -> bool:
        """Return true if the username input field has focus."""
        return get_app().layout.has_focus(self._username_input)

    def focus_username_input(self) -> None:
        """Focus the username input field."""
        get_app().layout.focus(self._username_input)

    def has_focus(self) -> bool:
        """Returns true if the menu options have focus"""
        return get_app().layout.has_focus(self._menu_container)

    def focus(self) -> None:
        """Focus on the menu options"""
        get_app().layout.focus(self._menu_container)

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.send_challenge)),
            ("class:function-bar.label", f"{'Send challenge':<14}", handle_mouse_click(self.send_challenge)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Creates the key bindings associated to the function bar fragments"""
        kb = KeyBindings()
        kb.add(Keys.F1, eager=True)(handle_bound_key_pressed(self.send_challenge))
        return kb

    def send_challenge(self) -> None:
        """Validate the username input and send the challenge if valid."""
        self._username_input.buffer.validate_and_handle()

    def _accept_username(self, _: Buffer) -> bool:
        """Handle Enter in the username input by validating and submitting."""
        self.presenter.handle_start_game()
        return True
