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
from cli_chess.utils.ui_common import handle_mouse_click, exit_app
from cli_chess.utils import is_linux_os, default, log
from prompt_toolkit import print_formatted_text as pt_print, HTML
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, Window, Container, FormattedTextControl, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.widgets import Box
from prompt_toolkit.styles import Style
from prompt_toolkit.output.color_depth import ColorDepth
try:
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError # noqa
except AssertionError:
    pass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainPresenter

main_view: Container


class MainView:
    def __init__(self, presenter: MainPresenter):
        try:
            self.presenter = presenter
            self._container = self._create_main_container()
            self.app = Application(
                layout=Layout(self._container),
                color_depth=ColorDepth.TRUE_COLOR if is_linux_os() else ColorDepth.DEFAULT,
                mouse_support=True,
                full_screen=True,
                style=Style.from_dict(default),
                refresh_interval=0.5
            )

            global main_view
            main_view = self

        except Exception as e:
            log.critical(f"Error starting cli-chess: {e}")
            if isinstance(e, NoConsoleScreenBufferError):
                print("Error starting cli-chess:\n"
                      "A Windows console was expected and not found.\n"
                      "Try running this program using cmd.exe instead.")
            else:
                print(f"Error starting cli-chess:\n{e}")
            exit(1)

    def run(self) -> None:
        """Runs the main application"""
        self.app.run()

    def _create_main_container(self):
        """Creates the container for the main view"""
        return HSplit([
            VSplit([
                Box(self.presenter.main_menu_presenter.view, padding=0, padding_right=1),
            ]),
            HSplit([
                self._create_function_bar()
            ], align=VerticalAlign.BOTTOM)
        ], key_bindings=self._create_function_bar_key_bindings())

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments = self.presenter.main_menu_presenter.view.get_function_bar_fragments()

            if fragments:
                fragments.append(("class:function-bar.spacer", " "))

            fragments.extend([
                ("class:function-bar.key", "F10", handle_mouse_click(exit_app)),
                ("class:function-bar.label", f"{'Quit':<14}", handle_mouse_click(exit_app))
            ])

            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
            Window(FormattedTextControl(f"cli-chess {__version__}"), align=WindowAlign.RIGHT)
        ], height=D(max=1, preferred=1))

    def _create_function_bar_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821
        """Creates the key bindings for the function bar"""
        main_menu_fb_key_bindings = self.presenter.main_menu_presenter.view.get_function_bar_key_bindings()

        # Always included key bindings
        always_included_bindings = KeyBindings()
        always_included_bindings.add(Keys.F10)(exit_app)

        return merge_key_bindings([main_menu_fb_key_bindings, always_included_bindings])

    @staticmethod
    def print_error_to_terminal(msg: str, error_header="Error:"):
        """Print an in terminal message. This is only to be used
           when the main application is not running yet. Set error
           parameter to True to highlight error messages.
        """
        pt_print(HTML(f"<red>{error_header}</red> {msg}"))

    def __pt_container__(self) -> Container:
        """Return the view container"""
        return self._container
