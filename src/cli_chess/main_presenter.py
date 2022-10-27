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

from cli_chess import MainModel, MainView
from cli_chess.menus.root_menu import RootMenuModel, RootMenuPresenter
from cli_chess.utils import lichess_config, is_valid_lichess_token, log


class MainPresenter:
    """Main entrypoint for starting the application and
       presenter logic for the startup layout
    """
    def __init__(self, model: MainModel):
        self.model = model
        self.view = MainView(self)
        self._handle_startup_args()

    def _handle_startup_args(self):
        """Handles the arguments passed in at startup to determine entrypoint"""
        args = self.model.startup_args

        if args.api_token:
            valid_token, msg = is_valid_lichess_token(args.api_token)
            if valid_token:
                lichess_config.set_value(lichess_config.Keys.API_TOKEN, args.api_token)
            else:
                self.view.in_terminal_error(msg)
                exit(1)

        # EXAMPLE: Starting up with the MenuManager
        startup_presenter = RootMenuPresenter(RootMenuModel())
        self.view.create_app(startup_presenter.view)

    def run(self):
        """Starts the main application"""
        self.view.app.run()
