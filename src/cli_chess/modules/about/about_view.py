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
from cli_chess.__metadata__ import __version__
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.layout import Window, VSplit, HSplit, D, FormattedTextControl, Container
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples, ANSI, HTML
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.about import AboutPresenter

CLI_CHESS_LINES = ANSI("\x1b[48;2;236;60;45;38;2;236;60;45m▄▄▄▄▄▄▄▄\n"
                       "\x1b[48;2;242;109;53;38;2;242;109;53m▄▄▄▄▄▄▄▄▄▄▄\n"
                       "\x1b[48;2;249;200;133;38;2;249;200;133m▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n"
                       "\x1b[48;2;41;170;225;38;2;41;170;225m▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")


class AboutView:
    def __init__(self, presenter: AboutPresenter):
        self.presenter = presenter
        self._container = self._create_container()

    @staticmethod
    def _create_container() -> Container:
        """Creates the container for the token manager view"""
        return VSplit([
            HSplit([
                Window(FormattedTextControl(HTML("<b>Author:</b> Trevor Bayless")), dont_extend_width=True, dont_extend_height=True),
                Window(FormattedTextControl(HTML("<b>License:</b> GPL v3.0")), dont_extend_width=True, dont_extend_height=True),
                Window(FormattedTextControl(HTML(f"<b>Version:</b> {__version__}")), dont_extend_width=True, dont_extend_height=True),
            ]),
            Box(Window(FormattedTextControl(CLI_CHESS_LINES)), padding=0, padding_left=2, width=D(min=1))
        ], width=D(min=1, max=80))

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns a set of function bar fragments to use if
           this module is hooked up with a function bar
        """
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.open_github_url)),
            ("class:function-bar.label", f"{'Open Github':<15}", handle_mouse_click(self.presenter.open_github_url)),
            ("class:function-bar.spacer", " "),
            ("class:function-bar.key", "F2", handle_mouse_click(self.presenter.open_github_issue_url)),
            ("class:function-bar.label", f"{'Report a bug':<15}", handle_mouse_click(self.presenter.open_github_issue_url)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Returns a set of key bindings to use if this
           module is hooked up with a function bar
        """
        kb = KeyBindings()
        kb.add(Keys.F1)(handle_bound_key_pressed(self.presenter.open_github_url))
        kb.add(Keys.F2)(handle_bound_key_pressed(self.presenter.open_github_issue_url))
        return kb

    def __pt_container__(self) -> Container:
        return self._container
