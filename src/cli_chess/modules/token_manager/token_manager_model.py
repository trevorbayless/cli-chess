from cli_chess.utils.config import lichess_config
from cli_chess.utils import Event, log, threaded
from berserk import Client, TokenSession
import berserk.exceptions

linked_token_scopes = set()


class TokenManagerModel:
    def __init__(self):
        self.base_url = ""
        self.linked_account = ""
        self.e_token_manager_model_updated = Event()

    def set_base_url(self, url: str):
        """Sets the base URL for all requests to go to"""
        self.base_url = url
        log.debug(f"Base URL set to: {self.base_url}")

    @threaded
    def validate_existing_linked_account(self) -> None:
        """Queries the Lichess config file for an existing token. If a token
           exists, verification is attempted. Invalid data will be cleared.
        """
        try:
            existing_token = lichess_config.get_value(lichess_config.Keys.API_TOKEN)
            account = self.validate_token(existing_token)
            if account:
                self.save_account_data(api_token=existing_token, account_data=account, valid=True)
            else:
                self.save_account_data(api_token="", account_data={})
        except Exception as e:
            # Rather than the token being invalid, this means there was a
            # connection problem. Ignore so the existing token is not overridden.
            if not isinstance(e, berserk.exceptions.ApiError):
                log.error(f"Unexpected exception caught: {e}")

    def update_linked_account(self, api_token: str) -> bool:
        """Attempts to update the linked account using the passed in API token.
           If the token is deemed valid, the api token is saved to the Lichess
           configuration. Returns True on success. Existing account data is
           only overwritten on success.
         """
        if api_token:
            try:
                account = self.validate_token(api_token)
                if account:
                    log.info("Updating linked Lichess account")
                    self.save_account_data(api_token=api_token, account_data=account, valid=True)
                    return True
            except Exception as e:
                log.error(f"Error updating linked account: {e}")
                return False
        return False

    def validate_token(self, api_token: str) -> dict:
        """Validates the proper scopes are available for the passed in token.
           Returns the scopes and userId associated to the passed in token.
        """
        if api_token:
            session = TokenSession(api_token)
            oauth_client = Client(session, base_url=self.base_url).oauth
            try:
                token_data = oauth_client.test_tokens(api_token)

                if token_data.get(api_token):
                    found_scopes = set()
                    for scope in token_data[api_token]['scopes'].split(sep=","):
                        found_scopes.add(scope)

                    from cli_chess.core.api.api_manager import required_token_scopes
                    if found_scopes >= required_token_scopes:
                        global linked_token_scopes
                        linked_token_scopes.clear()
                        linked_token_scopes = found_scopes

                        log.info("Successfully authenticated with Lichess")
                        return token_data[api_token]
                    else:
                        log.error("Valid token but missing required scopes")

            except Exception as e:
                log.error(f"Error validating token: {e}")
                raise

    def save_account_data(self, api_token: str, account_data: dict, valid=False) -> None:
        """Saves the passed in lichess api token to the configuration.
           It is assumed the passed in token has already been verified
        """
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)
        if valid:
            self.linked_account = account_data.get('userId', "")
            self._handle_start_api(api_token)

        self._notify_token_manager_model_updated()

    def _handle_start_api(self, api_token: str) -> None:
        """Handles starting the API using the supplied token.
           This function should only ever be called by this model.
        """
        if api_token.strip():
            from cli_chess.core.api.api_manager import _start_api  # noqa
            _start_api(api_token, self.base_url)

    def _notify_token_manager_model_updated(self) -> None:
        """Notifies listeners of token manager model updates"""
        self.e_token_manager_model_updated.notify()


g_token_manager_model = TokenManagerModel()
