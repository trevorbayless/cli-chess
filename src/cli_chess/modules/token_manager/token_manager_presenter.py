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
from cli_chess.modules.token_manager import TokenManagerView
from cli_chess.utils.config import lichess_config
from cli_chess.utils.logging import log
import webbrowser
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.token_manager import TokenManagerModel

API_TOKEN_CREATION_URL = ("https://lichess.org/account/oauth/token/create?" +
                          "scopes[]=challenge:read&" +   # Used for reading and accepting challenges
                          "scopes[]=challenge:write&" +  # Used for creating challenges
                          "scopes[]=board:play&" +       # Used for playing games
                          "description=cli-chess+token")


class TokenManagerPresenter:
    def __init__(self, model: TokenManagerModel):
        self.model = model
        self.view = TokenManagerView(self)

    def save_api_token(self, api_token: str):
        """Save the valid API access token to the configuration"""
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)

    def open_token_creation_url(self):
        """Open the web browser to the token creation url"""
        try:
            webbrowser.get()
            webbrowser.open_new(API_TOKEN_CREATION_URL)
        except Exception as e:
            log.error(f"Web browser: {e}")
