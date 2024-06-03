from cli_chess.utils.logging import configure_logger
from cli_chess.utils import setup_argparse
from cli_chess.__metadata__ import __version__
from platform import python_version, system, release, machine


class MainModel:
    """Model for the main presenter"""
    def __init__(self):
        self._start_loggers()
        self.startup_args = self._parse_args()

    @staticmethod
    def _start_loggers():
        """Start the loggers"""
        log = configure_logger("cli-chess")
        log.info(f"cli-chess v{__version__} // python {python_version()}")
        log.info(f"System information: system={system()} // release={release()} // machine={machine()}")

        configure_logger("chess.engine")
        configure_logger("berserk")

    @staticmethod
    def _parse_args():
        """Parse the args passed in at startup"""
        return setup_argparse().parse_args()
