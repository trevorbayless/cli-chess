import argparse
from importlib import metadata
from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.output import ColorDepth

from cli_chess.ui import MainMenu
from cli_chess.ui import APITokenInput
from cli_chess import common_utils
from cli_chess import config


def setup_argparse() -> argparse.ArgumentParser:
    """Sets up argparse and returns the argparse object"""
    parser = argparse.ArgumentParser(description="cli-chess: Play chess in your terminal")
    parser.add_argument(
        "-t",
        "--api-token", type=str, help="Sets your Lichess API token to the value passed in."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=metadata.version("cli-chess"),
    )
    return parser


def run() -> None:
    # Parse the arguments passed in
    args = setup_argparse().parse_args()

    if args.api_token:
        if common_utils.is_valid_lichess_token(args.api_token):
            config.set_lichess_value(config.LichessKeys.API_TOKEN, args.api_token)
        else:
            return print(f"Invalid Lichess API Token: {args.api_token}")

    app = Application(layout=Layout(MainMenu()),
                      color_depth=ColorDepth.TRUE_COLOR,
                      mouse_support=True,
                      full_screen=True)
    app.run()


if __name__ == "__main__":
    run()
