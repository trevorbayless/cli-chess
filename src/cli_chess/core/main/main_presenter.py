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
from cli_chess.core.main.main_view import MainView
from cli_chess.menus.main_menu import MainMenuModel, MainMenuPresenter
from cli_chess.core.api.api_manager import required_token_scopes
from cli_chess.modules.token_manager.token_manager_model import g_token_manager_model
from cli_chess.utils import force_recreate_configs, print_program_config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainModel


class MainPresenter:
    def __init__(self, model: MainModel):
        self.model = model
        self.main_menu_presenter = MainMenuPresenter(MainMenuModel())
        self.view = MainView(self)
        self._handle_startup_args()

    def _handle_startup_args(self):
        """Handles the arguments passed"""
        args = self.model.startup_args

        if args.print_config:
            print_program_config()
            exit(0)

        if args.reset_config:
            force_recreate_configs()

        if args.token:
            if not g_token_manager_model.update_linked_account(args.token):
                self.view.print_error_to_terminal(f"Invalid API token or missing required scopes. Scopes required: {required_token_scopes}", error=True)
                exit(1)

    def run(self):
        """Starts the main application"""
        self.view.run()
