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
from cli_chess.utils import log
from cli_chess.utils.ui_common import handle_mouse_click, go_back_to_main_menu, exit_app
from prompt_toolkit.widgets import TextArea, Box
from prompt_toolkit.layout import Window, Container, FormattedTextControl, ConditionalContainer, HSplit, VSplit, VerticalAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import to_filter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GamePresenterBase, PlayableGamePresenterBase


class GameViewBase:
    def __init__(self, presenter: GamePresenterBase) -> None:
        self.presenter = presenter
        self.board_output_container = presenter.board_presenter.view
        self.move_list_container = presenter.move_list_presenter.view
        self.material_diff_upper_container = presenter.material_diff_presenter.view_upper
        self.material_diff_lower_container = presenter.material_diff_presenter.view_lower
        self.player_info_upper_container = presenter.player_info_presenter.view_upper
        self.player_info_lower_container = presenter.player_info_presenter.view_lower
        self.error_label = FormattedTextControl(text="", style="class:label.error.banner", show_cursor=False)
        self.error_container = self._create_error_container()
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return Window(FormattedTextControl("Parent class needs to override _create_container()"))

    def _base_function_bar_fragments(self) -> StyleAndTextTuples:
        """Return the base function bar fragments"""
        return ([
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.flip_board)),
            ("class:function-bar.label", f"{'Flip board':<11}", handle_mouse_click(self.presenter.flip_board)),
            ("class:function-bar.spacer", " ")
        ])

    def _create_function_bar(self) -> VSplit:
        """Creates the views function bar"""
        return VSplit([
            Window(FormattedTextControl(self._base_function_bar_fragments())),
        ], height=D(max=1, preferred=1))

    def _container_key_bindings(self) -> KeyBindings:
        """Creates the key bindings for this container"""
        bindings = KeyBindings()

        @bindings.add(Keys.F1, eager=True)
        def _(event): # noqa
            self.presenter.flip_board()

        return bindings

    def _create_error_container(self) -> ConditionalContainer:
        """Create the error container"""
        return ConditionalContainer(
            Window(
                self.error_label,
                always_hide_cursor=True,
                height=D(max=1)
            ),
            filter=to_filter(False)
        )

    def show_error(self, text: str) -> None:
        """Displays the error label with the text passed in"""
        self.error_label.text = text
        self.error_container.filter = to_filter(True)

    def clear_error(self) -> None:
        """Clears the error containers"""
        self.error_label.text = ""
        self.error_container.filter = to_filter(False)

    @staticmethod
    def exit() -> None:
        """Exits this view and returns to the main menu"""
        go_back_to_main_menu()

    def __pt_container__(self) -> Container:
        """Return the view container"""
        return self._container


class PlayableGameViewBase(GameViewBase):
    """Implements a base game view which has a move input field"""
    def __init__(self, presenter: PlayableGamePresenterBase):
        self.presenter = presenter
        self.input_field_container = self._create_input_field_container()
        super().__init__(presenter)

    def _create_container(self) -> Container:
        main_content = Box(
            HSplit([
                VSplit([
                    self.board_output_container,
                    HSplit([
                        self.player_info_upper_container,
                        self.material_diff_upper_container,
                        self.move_list_container,
                        self.material_diff_lower_container,
                        self.player_info_lower_container
                    ])
                ]),
                self.input_field_container,
                self.error_container,
            ]),
            padding=1,
            padding_bottom=0
        )
        function_bar = HSplit([
            self._create_function_bar()
        ], align=VerticalAlign.BOTTOM)

        return HSplit([main_content, function_bar], key_bindings=self._container_key_bindings())

    def _container_key_bindings(self) -> KeyBindings:
        """Creates the key bindings for this container"""
        bindings = super()._container_key_bindings()

        @bindings.add(Keys.Up, eager=True)
        def _(event):  # noqa
            self.presenter.move_list_presenter.scroll_up()

        @bindings.add(Keys.Down, eager=True)
        def _(event):  # noqa
            self.presenter.move_list_presenter.scroll_down()

        return bindings

    def _create_input_field_container(self) -> TextArea:
        """Returns a TextArea to use as the input field"""
        input_field = TextArea(height=D(max=1),
                               prompt="Move:",
                               style="class:move-input",
                               multiline=False,
                               wrap_lines=True,
                               focus_on_click=True)

        input_field.accept_handler = self._accept_input
        return input_field

    def _accept_input(self, input: Buffer) -> None: # noqa
        """Accept handler for the input field"""
        # TODO: Remove this as it's for testing only
        if input.text == "quit":
            log.debug("User quit")
            exit_app()
        else:
            self.presenter.user_input_received(input.text)
            self.input_field_container.text = ''

    def lock_input(self) -> None:
        """Sets the input field to read only"""
        self.input_field_container.read_only = True

    def unlock_input(self) -> None:
        """Removes the read-only flag from the input field"""
        self.input_field_container.read_only = False
