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

from cli_chess import is_valid_lichess_token
from cli_chess.utils.config import lichess_config
from cli_chess.menus import MainMenu
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea, Label, Button, Dialog, ValidationToolbar
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.validation import Validator
# import webbrowser

API_TOKEN_CREATION_URL = ("https://lichess.org/account/oauth/token/create?" +
                          "scopes[]=challenge:read&" +   # Used for reading and accepting challenges
                          "scopes[]=challenge:write&" +  # Used for creating challenges
                          "scopes[]=board:play&" +       # Used for playing games
                          "description=cli-chess+token")

api_token_validator = Validator.from_callable(
    is_valid_lichess_token,
    error_message="Invalid Lichess API token.",
    move_cursor_to_end=True,
)


class APITokenInput:
    """Class to create the API Token Input screen"""
    def __init__(self):
        self.input = self.create_text_input()
        self.ok_button = Button(text="Ok", handler=self.ok_handler)
        self.cancel_button = Button(text="Cancel", handler=self.cancel_handler)
        self.dialog = self.create_dialog()

    def create_text_input(self) -> TextArea:
        """Create the text input area"""
        return TextArea(multiline=False,
                        focus_on_click=True,
                        validator=api_token_validator,
                        accept_handler=self._valid_token)

    def create_dialog(self) -> Dialog:
        """Create the Dialog wrapper"""
        return Dialog(title="Lichess API Token",
                      body=HSplit(
                          [
                              Label(text="Input your Lichess API token and press [ENTER]:", dont_extend_height=True),
                              self.input,
                              ValidationToolbar(),
                          ],
                          padding=D(preferred=1, max=1),
                      ),
                      buttons=[self.cancel_button],
                      with_background=True)

    def _valid_token(self, buf) -> None:
        """Called when the token is verified. Save the valid
           token to the configuration file.
        """
        api_token = self.input.text
        lichess_config.set_value(lichess_config.Keys.API_TOKEN, api_token)

    def ok_handler(self) -> str:
        """Handler for the 'Ok' button.
           Returns the validated API Token
        """
        return self.input.text

    def cancel_handler(self) -> None:
        """Handler for the 'Cancel' button"""
        MainMenu()

    def __pt_container__(self) -> Dialog:
        """Returns the dialog for container use"""
        return self.dialog
