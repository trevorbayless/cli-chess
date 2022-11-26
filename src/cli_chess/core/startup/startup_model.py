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

from cli_chess.utils.logging import configure_logger
from cli_chess.utils import setup_argparse
from cli_chess.__metadata__ import __version__


class StartupModel:
    """Model for the startup presenter"""
    def __init__(self):
        self._setup_logger()
        self.startup_args = self._parse_args()

    @staticmethod
    def _setup_logger():
        """Set up the root logger"""
        log = configure_logger("cli-chess")
        log.info(f"cli-chess v{__version__}")

    @staticmethod
    def _parse_args():
        """Parse the args passed in at startup"""
        return setup_argparse().parse_args()
