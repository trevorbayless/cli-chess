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
from cli_chess.core.startup import StartupView
from cli_chess.core.main import MainModel, MainPresenter
from cli_chess.core.api import required_token_scopes
from cli_chess.modules.token_manager import TokenManagerModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.startup import StartupModel

main_presenter = MainPresenter(MainModel())


class StartupPresenter:
    def __init__(self, model: StartupModel):
        self.model = model
        self.view = StartupView(self)
        self._handle_startup_args()

    def _handle_startup_args(self):
        """Handles the arguments passed in at startup to determine entrypoint"""
        args = self.model.startup_args

        if args.token:
            if not TokenManagerModel().update_linked_account(args.token):
                self.view.in_terminal_error(f"Invalid API token or missing required scopes. Scopes required: {required_token_scopes}")
                exit(1)

        # EXAMPLE: Starting up with the Main layout
        self.view.create_app(main_presenter.view)

    def run(self):
        """Starts the main application"""
        self.view.run()
