import os
import berserk
from prompt_toolkit.widgets import Label
from prompt_toolkit.layout import AnyContainer, VSplit


def is_unix_system():
    """Returns True if on a unix system"""
    return False if os.name == "nt" else True


def is_valid_lichess_token(api_token):
    """Returns True if the api token passed in is valid"""
    session = berserk.TokenSession(api_token)
    client = berserk.clients.Account(session)

    try:
        if client.get():
            return True
    except Exception:
        return False


def handle_api_exceptions(e):
    #TODO: Handle specific exceptions
    if e.message != "":
        if "No such token" in e.message:
            print("!! Invalid Lichess API token")
        elif "No such game" in e.message:
            print("Invalid game-id")
        elif "Not your game" in e.message:
            print("!! This game is not assocaited with your account")
        else:
            print(e)
    else:
        print(e)


def create_title(text: str, dont_extend_width: bool = False) -> Label:
    return Label(text, style="fg:ansiblue", dont_extend_width=dont_extend_width)


def indent_container(container: AnyContainer, amount: int = 2) -> AnyContainer:
    return VSplit([Label("", width=amount), container])
