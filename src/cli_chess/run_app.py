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

from cli_chess.menus import MainMenuPresenter
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from prompt_toolkit.output.color_depth import ColorDepth


async def run_app() -> None:
    app = Application(layout=Layout(MainMenuPresenter().view),
                      color_depth=ColorDepth.TRUE_COLOR,
                      mouse_support=True,
                      full_screen=True)

    await app.run_async()
