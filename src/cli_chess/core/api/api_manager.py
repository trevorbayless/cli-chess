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

from cli_chess.core.api.incoming_event_manger import IncomingEventManager
from cli_chess.utils.logging import log
from berserk import Client, TokenSession
from typing import Optional

API_TOKEN_CREATION_URL = ("https://lichess.org/account/oauth/token/create?" +
                          "scopes[]=challenge:read&" +
                          "scopes[]=challenge:write&" +
                          "scopes[]=board:play&" +
                          "description=cli-chess+token")

required_token_scopes: set = {"board:play", "challenge:read", "challenge:write"}

api_session: Optional[TokenSession]
api_client: Optional[Client]
api_iem: Optional[IncomingEventManager]
api_ready = False


def _start_api(token: str):
    """Handles creating a new API session, client, and IEM
       when the API token has been updated. This generally
       should only ever be called via the Token Manager on
       token verification.
    """
    global api_session, api_client, api_iem, api_ready
    try:
        api_session = TokenSession(token)
        api_client = Client(api_session)
        api_iem = IncomingEventManager()
        api_iem.start()
        api_ready = True
    except Exception as e:
        log.exception(f"api_manager: Failed to start api: {e}")


def api_is_ready() -> bool:
    """Check the status of the api connection. Currently,
       this is used for toggling the online menu availability
    """
    return api_ready
