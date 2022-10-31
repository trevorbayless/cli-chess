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
from cli_chess.core.startup import StartupView
from cli_chess.core.main import MainModel, MainPresenter
from cli_chess.utils import lichess_config, is_valid_lichess_token, log
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.startup import StartupModel


class StartupPresenter:
    def __init__(self, model: StartupModel):
        self.model = model
        self.view = StartupView(self)
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

        # EXAMPLE: Starting up with the Main layout
        main_presenter = MainPresenter(MainModel())
        self.view.create_app(main_presenter.view)

    def run(self):
        """Starts the main application"""
        self.view.app.run()
