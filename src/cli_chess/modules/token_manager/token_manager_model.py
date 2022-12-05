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
    def is_lichess_token_valid(self, api_token: str, save=True) -> bool:
        """Returns True if the api token passed in is valid. By default, this method
           will save valid credentials to the configuration file.
        """
        if api_token:
            session = TokenSession(api_token)
            account = clients.Account(session)

            try:
                account_data = account.get()
                if account_data:
                    log.info("Successfully authenticated with Lichess")
                    if save:
                        self.save_lichess_user(api_token, account_data['username'])
                    return True
            except BerserkError as e:
                log.error(f"Authentication to Lichess failed - {e.message}")
        return False

    @staticmethod
    def save_lichess_user(api_token: str, username: str) -> None:
        """Saves the passed in lichess api token and username to the configuration.
           It is assumed the passed in token has already been verified
        """
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)
        lichess_config.set_value(lichess_config.Keys.USERNAME, username)

    @staticmethod
    def get_lichess_username() -> str:
        """Queries the lichess configuration to get the linked username"""
        return lichess_config.get_value(lichess_config.Keys.USERNAME)
