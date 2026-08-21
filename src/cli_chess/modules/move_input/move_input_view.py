from __future__ import annotations
from prompt_toolkit.layout import Window, Container, FormattedTextControl, HSplit, D
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.move_input import MoveInputPresenter


class MoveInputView:
    def __init__(self, presenter: MoveInputPresenter):
        self.presenter = presenter
        self._input_field_container = self._create_input_field_container()
        self._input_hint_window = self._create_input_hint_container()
        self._container = self._create_container()

        self._input_field_container.buffer.on_text_changed.add_handler(self._on_move_input_buffer_changed)

    def _create_input_field_container(self) -> TextArea:
        """Creates the container for the move input field"""
        return TextArea(height=D(max=1),
                        prompt="Move:",
                        style="class:move-input", # TODO: Update this to have it's own class
                        multiline=False,
                        wrap_lines=True,
                        focus_on_click=True)

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
        ])

    def _on_move_input_buffer_changed(self, buffer: Buffer) -> None:
        self.presenter.on_move_input_changed(buffer.text)

    def _move_input_hint_fragments(self) -> StyleAndTextTuples:
        text = self.presenter.get_move_input_hint_text()
        return [("class:label.dim", text)] if text else []

    # def update(self, is_ticking: bool) -> None:
    #     """Updates the clock style using the data passed in"""
    #     if is_ticking:
    #         self._clock_control.style = "class:clock.ticking"
    #     else:
    #         self._clock_control.style = "class:clock"

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
