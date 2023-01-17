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
from cli_chess.utils.ui_common import go_back_to_main_menu, exit_app
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout import Window, Container, FormattedTextControl, ConditionalContainer, HSplit, VSplit, D
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import to_filter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GamePresenterBase, PlayableGamePresenterBase


class GameViewBase:
    def __init__(self, presenter: GamePresenterBase) -> None:
        self.board_output_container = presenter.board_presenter.view
        self.move_list_container = presenter.move_list_presenter.view
        self.material_diff_upper_container = presenter.material_diff_presenter.view_upper
        self.material_diff_lower_container = presenter.material_diff_presenter.view_lower
        self.error_label = FormattedTextControl(text="", style="class:label.error.banner", show_cursor=False)
        self.error_container = self._create_error_container()
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return Window(FormattedTextControl("Parent class needs to override _create_container()"))

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
    def exit_view() -> None:
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
        return HSplit([
            VSplit([
                self.board_output_container,
                HSplit([
                    self.material_diff_upper_container,
                    self.move_list_container,
                    self.material_diff_lower_container,
                ])
            ]),
            self.input_field_container,
            self.error_container
        ])

    def _create_input_field_container(self) -> TextArea:
        """Returns a TextArea to use as the input field"""
        input_type = "GAME"
        input_field = TextArea(height=D(max=1),
                               prompt=HTML(f"<style bg='darkcyan'>[{input_type}] $ </style>"),
                               style="class:input-field",
                               multiline=False,
                               wrap_lines=True,
                               focus_on_click=True)

        input_field.accept_handler = self._accept_input
        return input_field

    def _accept_input(self, input: Buffer) -> None:
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
