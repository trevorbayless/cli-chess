import argparse
from cli_chess.__metadata__ import __name__, __version__, __description__
from cli_chess.utils.logging import log, redact_from_logs
from cli_chess.utils.config import get_config_path
from cli_chess.core.api import required_token_scopes


class ArgumentParser(argparse.ArgumentParser):
    """The main ArgumentParser class (inherits argparse.ArgumentParser).
       This allows for parsed arguments strings to be added to the log
       redactor in order to safely log parsed arguments (e.g. redacting API keys)
    """
    def parse_args(self, args=None, namespace=None):
        """Override default parse_args method to allow for parsed
           arguments to be added to the log redactor
        """
        arguments = super().parse_args(args, namespace)
        if arguments.token:
            redact_from_logs(arguments.token)

        log.debug(f"Parsed arguments: {arguments}")
        return arguments


def setup_argparse() -> ArgumentParser:
    """Sets up argparse and parses the arguments passed in at startup"""
    parser = ArgumentParser(description=f"{__name__}: {__description__}")
    parser.add_argument(
        "--token",
        metavar="API_TOKEN",
        help=f"Links your Lichess API token with cli-chess. Scopes required: {required_token_scopes}",
        type=str
    )
    parser.add_argument(
        "--reset-config",
        help="Force resets the cli-chess configuration. Reverts the program to its default state.",
        action="store_true"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"cli-chess v{__version__}",
    )

    debug_group = parser.add_argument_group("debugging")
    debug_group.description = f"Program settings and logs can be found here: {get_config_path()}"
    debug_group.add_argument(
        "--base-url",
        metavar="URL",
        help="Point cli-chess requests to a different URL (e.g. http://localhost:8080)",
        default="https://lichess.org",
        type=str
    )
    debug_group.add_argument(
        "--print-config",
        help="Prints the cli-chess configuration file to the terminal and exits.",
        action="store_true"
    )

    return parser
