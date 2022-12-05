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
        self.model.e_token_manager_model_updated.add_listener(self.update)

    def update(self):
        """Updates the token manager view"""
        self.view.update(self.get_lichess_username())

    def is_lichess_token_valid(self, api_token: str) -> bool:
        """Calls the model to test api token validity. If the token is
           deemed valid, it is saved to the configuration file
        """
        return self.model.is_lichess_token_valid(api_token, save=True)

    def get_lichess_username(self) -> str:
        """Calls the model to get the username of the linked lichess account"""
        return self.model.get_lichess_username()
