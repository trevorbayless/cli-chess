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

import argparse
from cli_chess.__metadata__ import __version__
from cli_chess.utils.logging import redact_from_logs, log


class ArgumentParser(argparse.ArgumentParser):
    """The main ArgumentParser class (inherits argparse.ArgumentParser).
       This allows for parsed arguments strings to be added to the log
       redactor in order to safely log parsed arguments (e.g. redacting API keys)
    """
    def parse_args(self, args=None, namespace=None):
        """Override default parse_args method to allow for parsed
           arguments to be added to the log redactor
        """
        arguments = super().parse_args(args, namespace)
        if arguments.api_token:
            redact_from_logs(arguments.api_token)

        log.debug(f"Parsed arguments: {arguments}")
        return arguments


def setup_argparse() -> ArgumentParser:
    """Sets up argparse and parses the arguments passed in at startup"""
    parser = ArgumentParser(description="cli-chess: Play chess in your terminal")
    parser.add_argument(
        "-t",
        "--api-token", type=str, help="The API token associated to your Lichess account"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"cli-chess v{__version__}",
    )
    return parser
