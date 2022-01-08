import os
import berserk


def is_windows_system() -> bool:
    """Returns True if on a Windows system"""
    return True if os.name == "nt" else False


def is_valid_lichess_token(api_token: str) -> bool:
    """Returns True if the api token passed in is valid"""
    session = berserk.TokenSession(api_token)
    client = berserk.clients.Account(session)

    try:
        if client.get():
            return True
    except Exception:
        return False


def handle_api_exceptions(e: Exception) -> None:
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
