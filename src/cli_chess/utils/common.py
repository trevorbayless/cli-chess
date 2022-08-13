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

import os
import berserk
from cli_chess.utils.logging import log
from typing import Tuple


def is_windows_system() -> bool:
    """Returns True if on a Windows system"""
    return True if os.name == "nt" else False


def clear_screen() -> None:
    """Clears the terminal output"""
    os.system("cls") if is_windows_system() else os.system("clear")


def is_valid_lichess_token(api_token: str) -> Tuple[bool, str]:
    """Returns True if the api token passed in is valid"""
    session = berserk.TokenSession(api_token)
    client = berserk.clients.Account(session)

    try:
        if client.get():
            msg = "Successfully authenticated with Lichess"
            log.info(msg)
            return True, msg
    except Exception as e:
        msg = f"Authentication to Lichess failed - {e.message}"
        log.error(msg)
        return False, msg
