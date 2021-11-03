from enum import Enum
from cli_chess import is_valid_lichess_token
from cli_chess import config
from cli_chess.ui import MainMenu
from prompt_toolkit import HTML
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea, Label, Button, Dialog, ValidationToolbar
from prompt_toolkit.layout.containers import HSplit, AnyContainer
from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog, input_dialog
from prompt_toolkit.validation import Validator
import webbrowser


API_TOKEN_CREATION_URL = ("https://lichess.org/account/oauth/token/create?" +
                          "scopes[]=challenge:read&" +   # Used for reading and accepting challenges
                          "scopes[]=challenge:write&" +  # Used for creating challenges
                          "scopes[]=board:play&" +       # Used for playing games
                          "description=cli-chess+token" )


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
                        accept_handler=self.valid_token)


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


    def valid_token(self, buf) -> bool:
        """Called when the token is verified. Save the valid
           token to the configuration file.
        """
        api_token = self.input.text
        config.set_lichess_value(config.LichessKeys.API_TOKEN, api_token)


    def ok_handler(self) -> str:
        """Handler for the 'Ok' button.
           Returns the validated API Token
        """
        return self.input.text


    def cancel_handler(self) -> str:
        """Handler for the 'Cancel' button"""
        MainMenu()


    def __pt_container__(self) -> Dialog:
        """Returns the dialog for container use"""
        return self.dialog
