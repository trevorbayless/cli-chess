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

from cli_chess.utils.logging import log, redact_from_logs
from cli_chess.utils.config import lichess_config
from cli_chess.utils.event import Event
from berserk import TokenSession, clients
from berserk.exceptions import BerserkError


class TokenManagerModel:
    def __init__(self):
        self.e_token_manager_model_updated = Event()

    def validate_existing_account_data(self) -> None:
        """Queries the Lichess config file for an existing token. If a token
           exists, verification is attempted. The linked lichess username will
           be updated depending on validation. Invalid data will be cleared.
        """
        existing_token = lichess_config.get_value(lichess_config.Keys.API_TOKEN)
        account_data = self.get_account_data(existing_token)
        if account_data:
            self.save_account_data(api_token=existing_token, username=account_data['username'])
        else:
            self.save_account_data(api_token="", username="")

    def update_linked_account(self, api_token: str) -> bool:
        """Attempts to update the linked account using the passed in API token.
           If the token is deemed valid, the api token and username are saved
           to the Lichess configuration. Returns True on success. Existing
           account data is only overwritten on success.
         """
        if api_token:
            account_data = self.get_account_data(api_token)
            if account_data:
                log.info("Updating linked Lichess account")
                self.save_account_data(api_token, account_data['username'])
                return True
        return False

    @staticmethod
    def get_account_data(api_token: str) -> dict:
        """Returns user data when the passed in token is valid"""
        account_data = {}
        if api_token:
            session = TokenSession(api_token)
            account = clients.Account(session)
            try:
                account_data = account.get()
                log.info("Successfully authenticated with Lichess")
            except BerserkError as e:
                log.error(f"Authentication to Lichess failed - {e.message}")
        return account_data

    def save_account_data(self, api_token: str, username: str) -> None:
        """Saves the passed in lichess api token and username to the configuration.
           It is assumed the passed in token has already been verified
        """
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)
        lichess_config.set_value(lichess_config.Keys.USERNAME, username)
        self._notify_token_manager_model_updated()

    @staticmethod
    def get_linked_account_name() -> str:
        """Gets the name of the linked account"""
        return lichess_config.get_value(lichess_config.Keys.USERNAME)

    def _notify_token_manager_model_updated(self) -> None:
        """Notifies listeners of token manager model updates"""
        self.e_token_manager_model_updated.notify()
