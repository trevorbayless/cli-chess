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
from cli_chess.modules.board import BoardView
from cli_chess.modules.move_list import MoveListView
from cli_chess.modules.material_difference import MaterialDifferenceView
from cli_chess.utils import log
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout import Window, Container, FormattedTextControl, ConditionalContainer, HSplit, VSplit, D
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.application import get_app
from prompt_toolkit.filters import to_filter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core import GamePresenterBase


class GameViewBase:
    def __init__(self, game_presenter: GamePresenterBase, board_view: BoardView, move_list_view: MoveListView,
                 material_diff_upper_view: MaterialDifferenceView, material_diff_lower_view: MaterialDifferenceView) -> None:
        self.game_presenter = game_presenter
        self.board_output_container = board_view
        self.move_list_container = move_list_view
        self.material_diff_upper_container = material_diff_upper_view
        self.material_diff_lower_container = material_diff_lower_view
        self.input_field_container = self._create_input_field_container()
        self.error_label = FormattedTextControl(text="", style="class:label.error.banner", show_cursor=False)
        self.error_container = self._create_error_container()
        self.root_container = self._create_root_container()

    def _create_root_container(self) -> Container:
        return HSplit(
            [
                VSplit(
                    [
                        self.board_output_container,
                        HSplit(
                            [
                                self.material_diff_upper_container,
                                self.move_list_container,
                                self.material_diff_lower_container,
                            ]
                        )
                    ]),
                self.input_field_container,
                self.error_container
            ]
        )

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

    def _accept_input(self, input: Buffer) -> None:
        """Accept handler for the input field"""
        if input.text == "quit":
            log.debug("User quit")
            get_app().exit()
        else:
            self.game_presenter.user_input_received(input.text)
            self.input_field_container.text = ''

    def lock_input(self) -> None:
        """Sets the input field to read only"""
        self.input_field_container.read_only = True

    def unlock_input(self) -> None:
        """Removes the read-only flag from the input field"""
        self.input_field_container.read_only = False

    def show_error(self, text: str) -> None:
        """Displays the error label with the text passed in"""
        self.error_label.text = text
        self.error_container.filter = to_filter(True)

    def clear_error(self) -> None:
        """Clears the error containers"""
        self.error_label.text = ""
        self.error_container.filter = to_filter(False)
