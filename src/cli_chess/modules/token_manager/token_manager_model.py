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
from cli_chess.utils.config import lichess_config
from berserk import TokenSession, clients
from berserk.exceptions import BerserkError


class TokenManagerModel:
    def __init__(self):
        self.account_name: str = "None"

    def get_account_name(self) -> str:
        """Returns the account name linked to the saved API token"""
        api_token = lichess_config.get_value(lichess_config.Keys.API_TOKEN)
        if api_token:
            session = TokenSession(api_token)
            account = clients.Account(session)

            try:
                self.account_name = account.get()['id']
            except BerserkError:
                self.account_name = "None"

        return self.account_name

    def is_lichess_token_valid(self, api_token: str, save=False) -> bool:
        """Returns True if the api token passed in is valid. Passing in the 'save'
           parameter with 'True' will save the api token to the configuration file
           if it is valid
        """
        if api_token:
            session = TokenSession(api_token)
            account = clients.Account(session)

            try:
                if account.get():
                    log.info("Successfully authenticated with Lichess")
                    if save:
                        self.save_lichess_token(api_token)
                    return True
            except BerserkError as e:
                log.error(f"Authentication to Lichess failed - {e.message}")
        return False

    @staticmethod
    def save_lichess_token(api_token) -> None:
        """Save the passed in lichess api token to the configuration. It is assumed
           that the passed in token has already been verified
        """
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)
