# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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

from __future__ import annotations
from cli_chess.utils.logging import log
from platform import system
from typing import Tuple, Type
import threading
import subprocess
import enum
import os

VALID_COLOR_DEPTHS = ["DEPTH_24_BIT", "DEPTH_8_BIT", "DEPTH_4_BIT"]
COLOR_DEPTH_MAP = {
    "DEPTH_24_BIT": "True color",
    "DEPTH_8_BIT": "256 colors",
    "DEPTH_4_BIT": "ANSI colors"
}


class RequestSuccessfullySent(Exception):
    """Custom exception to use upon success of a call"""
    pass


class AlertType(enum.Enum):
    """General alert class which can be
       used for alert type classification
    """
    SUCCESS = enum.auto()
    NEUTRAL = enum.auto()
    ERROR = enum.auto()

    def get_style(self, alert_type: AlertType) -> str:
        """Returns the associated style for the passed in alert type"""
        if alert_type is self.SUCCESS:
            return "class:label.success.banner"
        elif alert_type is self.NEUTRAL:
            return "class:label.neutral.banner"
        else:
            return "class:label.error.banner"


def is_linux_os() -> bool:
    """Returns True if running on Linux"""
    return True if system() == "Linux" else False


def is_windows_os() -> bool:
    """Returns True if running on Windows"""
    return True if system() == "Windows" else False


def is_mac_os() -> bool:
    """Returns True if running on Mac"""
    return True if system() == "Darwin" else False


def str_to_bool(s: str) -> bool:
    """Returns a boolean based on the passed in string"""
    return s.lower() in ("true", "yes", "1")


def open_url_in_browser(url: str):
    """Open the passed in URL in the default web browser"""
    url = url.strip()
    if url:
        try:
            if is_windows_os():
                os.startfile(url)
            else:
                cmd = 'open' if is_mac_os() else 'xdg-open'
                subprocess.Popen([cmd, url],
                                 close_fds=True,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 start_new_session=True)
        except Exception as e:
            log.error(f"Common: Error opening URL in browser: {e}")


def threaded(fn):
    """Decorator for a threaded function"""
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper


def retry(times: int, exceptions: Tuple[Type[Exception], ...]):
    """Decorator to retry a function. Retries the wrapped function
       (x) times if the exceptions listed in `exceptions` are thrown.
       Example exceptions parameter: exceptions=(ValueError, KeyError)
    """
    def wrapper(func):
        def retry_fn(*args, **kwargs):
            attempt = 1
            while attempt <= times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    log.error(f"Exception when attempting to run {func}. Attempt {attempt} of {times}. Exception = {e}")
                    attempt += 1
            return func(*args, **kwargs)
        return retry_fn
    return wrapper
