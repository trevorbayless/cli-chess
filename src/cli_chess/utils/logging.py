import logging

log = logging.getLogger("cli-chess")
log_redactions = []


def configure_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """Configures and returns a logger instance"""
    from cli_chess.utils.config import get_config_path

    log_file = f"{get_config_path()}" + f"{name}.log"
    log_format = "%(asctime)s.%(msecs)03d | %(levelname)-5s | %(name)s | %(module)s.%(funcName)s | %(message)s"
    time_format = "%m/%d/%Y %I:%M:%S"

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(LoggingRedactor(log_format, time_format))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger


def redact_from_logs(text: str = "") -> None:
    """Adds the passed in text to the log redaction list"""
    text = text.strip()
    if text and text not in log_redactions:
        log_redactions.append(text)


class LoggingRedactor(logging.Formatter):
    """Log formatter that redacts matches from being logged.
       Loops through the `log_redactions` list and replaces the
       text before outputting it to the log (eg. API keys)
    """
    @staticmethod
    def _filter(text):
        redacted_text = text
        for item in log_redactions:
            redacted_text = redacted_text.replace(item, "********")
        return redacted_text

    def format(self, log_record):
        text = logging.Formatter.format(self, log_record)
        return self._filter(text)
