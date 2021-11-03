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


# def show_request_to_generate_token():
#     """Display a message box asking if the browser can
#        be opened to generate a Lichess API token. If 'Yes',
#        the Lichess website will be opened at the token creation URL.
#        If 'No', the prompt to input the API token will be displayed.
#     """
#     result = yes_no_dialog(
#         title="Generate Lichess API Token?",
#         text="A valid Lichess API token is required to connect with Lichess.\n" +
#               "To be taken to the Lichess site to generate your token, select 'Yes'.\n"
#               "Please keep all defaults set on the page and copy/paste your API token on the next screen.\n\n" +
#               "Are you ready to open the browser to generate your token?"
#     ).run()

#     if result:
#         webbrowser.open(API_TOKEN_CREATION_URL)

#     return show_api_token_input()


# def show_api_token_input():
#     """Show API token input screen"""
#     user_cancelled = None
#     api_token = input_dialog(
#         title='Lichess API Token',
#         text='Please input your Lichess API token:',
#         validator=api_token_validator,
#         ).run()

#     if not user_cancelled and is_valid_lichess_token(api_token):
#         config.set_lichess_value(config.LichessKeys.API_TOKEN, api_token)
#         return True
#     else:
#         return False