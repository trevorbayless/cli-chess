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

import logging

log = logging.getLogger("cli-chess")
log_redactions = []


def configure_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """Configures and returns a logger instance"""
    from cli_chess.utils.config import get_config_path

    log_file = f"{get_config_path()}" + f"{name}.log"
    log_format = "%(asctime)s.%(msecs)03d | %(levelname)-5s | %(name)s | %(module)s | %(message)s"
    time_format = "%m/%d/%Y %I:%M:%S"

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(LoggingRedactor(log_format, time_format))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger


def redact_from_logs(text: str = "") -> None:
    """Adds the passed in text to the log redaction list"""
    if text not in log_redactions and text != "":
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
