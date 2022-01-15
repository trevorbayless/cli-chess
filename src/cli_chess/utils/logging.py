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

from cli_chess.utils.config import get_config_path
import logging

log = logging.getLogger("cli-chess")


def start_logger() -> None:
    """Starts the root logger"""
    logging.basicConfig(level=logging.DEBUG,
                        filemode="w",
                        filename=f"{get_config_path()}" + "cli-chess.log",
                        format="%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S%p")
