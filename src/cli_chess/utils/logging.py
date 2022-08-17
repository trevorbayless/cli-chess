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


def start_logger() -> None:
    """Starts the root logger"""
    from cli_chess.utils.config import get_config_path
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s"
    logging.basicConfig(level=logging.DEBUG,
                        filemode="w",
                        filename=f"{get_config_path()}" + "cli-chess.log",
                        datefmt="%m/%d/%Y %I:%M:%S%p")

    for handler in logging.root.handlers:
        handler.setFormatter(LoggingRedactor(log_format))


def redact_from_logs(text: str = "") -> None:
    """Adds the passed in text to the log redaction list"""
    if text not in log_redactions and text is not None:
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
