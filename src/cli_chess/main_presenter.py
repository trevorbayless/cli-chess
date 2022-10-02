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
from cli_chess.menus.root_menu import RootMenuPresenter
from cli_chess.utils import setup_argparse, lichess_config, is_valid_lichess_token


class MainPresenter:
    """Main entrypoint for starting the application and
       presenter logic for the startup layout
    """
    def __init__(self):
        self.model = MainModel()
        self.view = MainView(self)
        self.parse_startup_args()  # Todo: Handle this in the model?

    def parse_startup_args(self):
        """Parse the arguments passed in at startup to determine entrypoint"""
        # Todo: Parse passed in arguments
        args = setup_argparse().parse_args()

        if args.api_token:
            valid_token, msg = is_valid_lichess_token(args.api_token)
            if valid_token:
                lichess_config.set_value(lichess_config.Keys.API_TOKEN, args.api_token)
            else:
                print(msg)  # Todo: Pass this to the view for formatting text
                exit(1)

        # EXAMPLE: Starting up with the MenuManager
        # Todo: Move this logic into a separate function
        startup_presenter = RootMenuPresenter()
        self.view.create_app(startup_presenter.view, startup_presenter.view.key_bindings)

    def run(self):
        """Starts the main application"""
        self.view.app.run()
