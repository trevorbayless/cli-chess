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
from cli_chess.utils import is_valid_lichess_token
from cli_chess.utils.config import lichess_config
from cli_chess.utils.argparse import setup_argparse
from cli_chess.utils.logging import configure_logger

def run() -> None:
    """Main entry point"""
    configure_logger("cli-chess")
    args = setup_argparse().parse_args()

    if args.api_token:
        valid_token, msg = is_valid_lichess_token(args.api_token)
        if valid_token:
            lichess_config.set_value(lichess_config.Keys.API_TOKEN, args.api_token)
        else:
            print(msg)
            exit(1)

    MainMenuPresenter().show_menu()

if __name__ == "__main__":
    run()
