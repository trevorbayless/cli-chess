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
from cli_chess.utils import default_style
from prompt_toolkit.layout import Layout, Container
from prompt_toolkit.application import Application, DummyApplication
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.output.color_depth import ColorDepth
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess import MainPresenter


class MainView:
    """Starts the application with the initial layout"""
    def __init__(self, presenter: MainPresenter):
        self.app = DummyApplication()
        self.presenter = presenter

    def create_app(self, initial_container: Container, initial_key_bindings: KeyBindings):
        """Create the main application"""
        self.app = Application(
            layout=Layout(initial_container),
            key_bindings=initial_key_bindings,
            color_depth=ColorDepth.TRUE_COLOR,
            mouse_support=True,
            full_screen=True,
            style=Style.from_dict(default_style)
        )

    def quit(self):
        """Quit the application"""
        self.app.exit()