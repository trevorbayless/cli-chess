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
from cli_chess.utils import is_linux_os, default
from prompt_toolkit.layout import Layout, Container
from prompt_toolkit.application import Application, DummyApplication, get_app
from prompt_toolkit import print_formatted_text as pt_print, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.output.color_depth import ColorDepth
try:
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError # noqa
except AssertionError:
    pass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.startup import StartupPresenter


class StartupView:
    """Starts the application with the initial layout"""
    def __init__(self, presenter: StartupPresenter):
        self.app = DummyApplication()
        self.presenter = presenter

    def create_app(self, initial_container: Container):
        """Create the main application with the initial layout"""
        try:
            self.app = Application(
                layout=Layout(initial_container),
                color_depth=ColorDepth.TRUE_COLOR if is_linux_os() else ColorDepth.DEFAULT,
                mouse_support=True,
                full_screen=True,
                style=Style.from_dict(default)
            )
        except NoConsoleScreenBufferError:
            print("Error starting cli-chess:\n"
                  "A Windows console was expected and not found.\n"
                  "Try running this program using cmd.exe instead.")
            exit(1)

    @staticmethod
    def print_in_terminal_msg(msg: str, error=False):
        """Print an in terminal message. This is only to be used
           when the main application is not running yet. Set error
           parameter to True to highlight error messages.
        """
        if not get_app().is_running:
            if not error:
                pt_print(f"{msg}")
            else:
                pt_print(HTML(f"<red>Error:</red> {msg}"))

    def run(self) -> None:
        """Runs the main application"""
        self.app.run()
