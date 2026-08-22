from __future__ import annotations
from cli_chess.utils.ui_common import repaint_ui
from prompt_toolkit.layout import Window, Container, FormattedTextControl, HSplit, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import has_focus
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.game_input_field import GameInputPresenter
    from prompt_toolkit.buffer import Buffer


class GameInputView:
    def __init__(self, presenter: GameInputPresenter):
        self.presenter = presenter
        self._input_field_container = self._create_input_field_container()
        self._input_field_container.buffer.on_text_changed.add_handler(self._on_move_input_buffer_changed)
        self._input_hint_window = self._create_input_hint_container()

        self.key_bindings = self._create_key_bindings()
        self._container = self._create_container()

    def _create_input_field_container(self) -> TextArea:
        """Creates the container for the move input field"""
        input_field =  TextArea(height=D(max=1),
                                prompt="Move:",
                                style="class:move-input", # TODO: Update this to have it's own class
                                multiline=False,
                                wrap_lines=True,
                                focus_on_click=True)

        input_field.accept_handler = self._accept_input
        return input_field

    def _create_input_hint_container(self):
        """Creates the container for the input hint"""
        return Window(
            FormattedTextControl(lambda: self._move_input_hint_fragments()),
            height=D(max=1),
        )

    def _create_container(self) -> Container:
        """Creates the container for the move input field"""
        return HSplit([
            self._input_field_container,
            self._input_hint_window,
            #ConditionalContainer(self.input_hint_window, to_filter(not self.show))
        ], height=D(max=2, preferred=2))

    def _create_key_bindings(self) -> KeyBindings:
        """Create the key bindings for the move input container"""
        bindings = KeyBindings()

        @bindings.add(Keys.Tab, filter=has_focus(self._input_field_container), eager=True)
        def _(event):
            if self.presenter.try_tab_complete_move_input(self._input_field_container.buffer):
                repaint_ui()

        return bindings

    def _on_move_input_buffer_changed(self, buffer: Buffer) -> None:
        self.presenter.on_move_input_changed(buffer.text)

    def _move_input_hint_fragments(self) -> StyleAndTextTuples:
        text = self.presenter.get_move_input_hint_text()
        return [("class:label.dim", text)] if text else []

    def _accept_input(self, input: Buffer) -> None: # noqa
        """Accept handler for the input field"""
        self.presenter.input_received(input.text)
        self._input_field_container.text = ''

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
