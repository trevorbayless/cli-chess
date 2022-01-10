from cli_chess.utils.config import get_config_path
import logging

log = logging.getLogger("cli-chess")


def start_logger() -> None:
    """Starts the root logger"""
    logging.basicConfig(level=logging.DEBUG,
                        filemode="w",
                        filename=f"{get_config_path()}" + "cli-chess.log",
                        format="%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S%p")
