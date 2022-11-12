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

from cli_chess.utils.logging import log
from os import name as os_name
from berserk import TokenSession, clients
from berserk.exceptions import BerserkError


def is_windows_system() -> bool:
    """Returns True if on a Windows system"""
    return True if os_name == "nt" else False


def is_valid_lichess_token(api_token: str) -> bool:
    """Returns True if the api token passed in is valid"""
    session = TokenSession(api_token)
    account = clients.Account(session)

    try:
        if account.get():
            log.info("Successfully authenticated with Lichess")
            return True
    except BerserkError as e:
        log.error(f"Authentication to Lichess failed - {e.message}")
        return False
