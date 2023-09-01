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

from __future__ import annotations
from cli_chess.modules.token_manager import TokenManagerView
from cli_chess.utils.common import open_url_in_browser
from cli_chess.core.api.api_manager import required_token_scopes
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.token_manager import TokenManagerModel


class TokenManagerPresenter:
    def __init__(self, model: TokenManagerModel):
        self.model = model
        self.view = TokenManagerView(self)
        self.model.e_token_manager_model_updated.add_listener(self.update)
        self.model.validate_existing_linked_account()

    def update(self):
        """Updates the token manager view"""
        self.view.lichess_username = self.model.linked_account

    def update_linked_account(self, api_token: str) -> bool:
        """Calls the model to test api token validity. If the token is
           deemed valid, it is saved to the configuration file
        """
        return self.model.update_linked_account(api_token)

    def open_token_creation_url(self) -> None:
        """Open the URL to create a Lichess API token"""
        url = f"{self.model.base_url}/account/oauth/token/create?"

        for scope in required_token_scopes:
            url = url + f"scopes[]={scope}&"

        url = url + "description=cli-chess+token"
        open_url_in_browser(url)
