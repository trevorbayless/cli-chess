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

from cli_chess.utils import config, is_valid_lichess_token
from cli_chess.utils.logging import start_logger, redact_from_logs, log
from cli_chess import run_app
from importlib import metadata
import argparse
import asyncio

from cli_chess.menus import MainMenuPresenter


def run() -> None:
    """Main entry point"""
    start_logger()
    parse_args()

    while True:
        try:
            MainMenuPresenter().show_menu()

        except KeyboardInterrupt:
            # Todo: Need to handle keyboard interrupt within the menu presenter
            exit(0)


def parse_args() -> None:
    """Parse the arguments passed in at startup"""
    args = setup_argparse().parse_args()
    redact_from_logs(args.api_token)
    log.debug(f"parsed_args: {args}")

    if args.api_token:
        if is_valid_lichess_token(args.api_token):
            config.set_lichess_value(config.LichessKeys.API_TOKEN, args.api_token)
        else:
            msg = "Invalid Lichess API token entered"
            print(msg)
            log.error(msg)
            exit(1)


def setup_argparse() -> argparse.ArgumentParser:
    """Sets up argparse and returns the argparse object"""
    parser = argparse.ArgumentParser(description="cli-chess: Play chess in your terminal")
    parser.add_argument(
        "-t",
        "--api-token", type=str, help="The API token associated to your Lichess account"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=metadata.version("cli-chess"),
    )
    return parser


if __name__ == "__main__":
    run()
