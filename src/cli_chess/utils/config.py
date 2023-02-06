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

from cli_chess.utils.common import is_linux_os, is_windows_os
from cli_chess.utils.logging import log, redact_from_logs
from cli_chess.utils.event import Event
from os import path, makedirs
from getpass import getuser
from enum import Enum
import configparser

# TODO: Handle exceptions
# TODO: Handle new config options on updates (do not overwrite full config)
# TODO: Add a "force_update" to pull new values if they have been changed during runtime
DEFAULT_CONFIG_FILENAME = "config.ini"


def get_config_path() -> str:
    """Returns the config filepath to use based on OS"""
    file_path = "$HOME/.config/cli-chess/"

    if is_windows_os():
        file_path = "$APPDATA/cli-chess/"

    return path.expandvars(file_path)


class BaseConfig:
    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME) -> None:
        """Default base class constructor"""
        self.file_path = get_config_path()
        self.full_filename = self.file_path + filename
        self.parser = configparser.ConfigParser()
        self.parser.read(self.full_filename)

        # Event called on any configuration write event
        self.e_config_updated = Event()

    def write_config(self) -> None:
        """Writes to the configuration file"""
        if not path.exists(self.file_path):
            makedirs(self.file_path)

        with open(self.full_filename, 'w') as config_file:
            self.parser.write(config_file)
            self.e_config_updated.notify()

    def config_exists(self) -> bool:
        """Returns True if the configuration file exists"""
        return path.isfile(self.full_filename)

    def add_section(self, section: str) -> None:
        """Add a section to the configuration file"""
        self.parser[section] = {}
        self.write_config()

    def has_section(self, section: str) -> bool:
        """Returns true if the section passed in exists in the configuration file"""
        return self.parser.has_section(section)

    def set_key_value(self, section: str, key: str, value: str) -> None:
        """Set (or add) a key/value to a section in the configuration file"""
        # TODO: Raise error if section does not exist
        self.parser[section][key] = str(value.strip() if isinstance(value, str) else value)
        self.write_config()

    def get_config_filename(self) -> str:
        """Returns the configuration filename"""
        return self.full_filename

    def get_key_value(self, section: str, key: str, lowercase: bool = True) -> str:
        """Retrieve the value at the passed in section/key pair"""
        try:
            key_value = self.parser.get(section, key).strip()
            if lowercase:
                key_value = key_value.lower()
            return key_value
        except Exception as e:
            self.handle_exception(e)

    def get_key_boolean_value(self, section: str, key: str) -> bool:
        """Retrieve the boolean value at the passed in section/key pair"""
        try:
            return self.parser.getboolean(section, key)
        except Exception as e:
            self.handle_exception(e)

    def get_sections_values(self, section: str) -> dict:
        """Returns a dictionary of all key/values at the section passed in.
           Since by default configparser dumps booleans as strings in the
           items() call, this function will handle the conversion to a proper boolean
        """
        boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                          '0': False, 'no': False, 'false': False, 'off': False}
        try:
            section_values = dict(self.parser.items(section))
            for key in section_values:
                if section_values[key].lower() in boolean_states:
                    section_values[key] = self.get_key_boolean_value(section, key)
            return section_values
        except Exception as e:
            self.handle_exception(e)

    @staticmethod
    def handle_exception(e: Exception) -> None:
        """Handles exceptions that occur while parsing the configuration file"""
        log.error(f"Exception caught while parsing the configuration file: {e}")


class SectionBase(BaseConfig):
    def __init__(self, section_name: str, section_keys, filename: str = DEFAULT_CONFIG_FILENAME):
        super().__init__(filename)
        self.section_name = section_name
        self.section_keys = section_keys
        self._verify_section_integrity()

    def _verify_section_integrity(self):
        # Todo: Update this to verify this section and all keys (has_option, has_section)
        if super().has_section(self.section_name):
            pass
        else:
            self._rebuild_section()

    def _rebuild_section(self) -> None:
        """Rebuild this section using key value defaults"""
        super().add_section(self.section_name)
        for key in self.section_keys:
            super().set_key_value(self.section_name, key.name, key.value["default"])

    def get_all_values(self) -> dict:
        """Returns a dictionary of all key/values in this section"""
        return super().get_sections_values(self.section_name)

    def get_value(self, key: Enum) -> str:
        """Get the value of the key passed in from the configuration file"""
        return super().get_key_value(self.section_name, key.name, False)

    def set_value(self, key, value: str) -> None:
        """Set a keys value in the configuration file"""
        super().set_key_value(self.section_name, key.name, value)

    def get_boolean(self, key) -> bool:
        """Retrieve the boolean value at the passed in section/key pair"""
        return super().get_key_boolean_value(self.section_name, key.name)


class PlayerInfoConfig(SectionBase):
    """Creates and manages the "player info" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        OFFLINE_PLAYER_NAME = {"name": "offline_player_name", "default": getuser() if getuser() else "You"}

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_player_info_config_updated = Event()
        super().__init__(section_name="player_info", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_player_info_config_updated.notify()


class BoardConfig(SectionBase):
    """Creates and manages the "board" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        SHOW_BOARD_COORDINATES = {"name": "show_board_coordinates", "default": True}
        SHOW_BOARD_HIGHLIGHTS = {"name": "show_board_highlights", "default": True}
        BLINDFOLD_CHESS = {"name": "blindfold_chess", "default": False}
        USE_UNICODE_PIECES = {"name": "use_unicode_pieces", "default": True}
        RANK_LABEL_COLOR = {"name": "rank_label_color", "default": "gray"}
        FILE_LABEL_COLOR = {"name": "file_label_color", "default": "gray"}
        LAST_MOVE_COLOR = {"name": "last_move_color", "default": "yellowgreen"}
        LIGHT_SQUARE_COLOR = {"name": "light_square_color", "default": "cadetblue"}
        DARK_SQUARE_COLOR = {"name": "dark_square_color", "default": "darkslateblue"}
        IN_CHECK_COLOR = {"name": "in_check_color", "default": "red"}
        LIGHT_PIECE_COLOR = {"name": "light_piece_color", "default": "white"}
        DARK_PIECE_COLOR = {"name": "dark_piece_color", "default": "black"}

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_board_config_updated = Event()
        super().__init__(section_name="board", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_board_config_updated.notify()


class UiConfig(SectionBase):
    """Creates and manages the "ui" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        ZEN_MODE = {"name": "zen_mode", "default": False}

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_ui_config_updated = Event()
        super().__init__(section_name="ui", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_ui_config_updated.notify()


class EngineConfig(SectionBase):
    """NOTE: This is not used currently as cli-chess for the time being only directly supports Fairy-Stockfish.
       Creates and manages the "engine" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        ENGINE_NAME = {"name": "engine_name", "default": "Fairy-Stockfish"}
        ENGINE_PATH = {"name": "engine_path", "default": path.join(path.realpath(__file__ + "/../../modules/engine/binaries"), '')}
        ENGINE_BINARY_NAME = {"name": "engine_binary_name", "default": "fairy-stockfish_14_x86-64_" + ("linux" if is_linux_os() else ("windows" if is_windows_os() else "mac"))}

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_engine_config_updated = Event()
        super().__init__(section_name="engine", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_engine_config_updated.notify()


class LichessConfig(SectionBase):
    """Creates and manages the "lichess" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        API_TOKEN = {"name": "api_token", "default": ""}
        USERNAME = {"name": "username", "default": ""}

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_lichess_config_updated = Event()
        super().__init__(section_name="lichess", section_keys=self.Keys, filename=filename)
        redact_from_logs(self.get_value(self.Keys.API_TOKEN))

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_lichess_config_updated.notify()

    def set_value(self, key, value: str) -> None:
        """Set a keys value in the configuration file. Overrides the base
           method to allow for API token log redaction if the value being
           set is an API token.
        """
        if key == self.Keys.API_TOKEN and value:
            redact_from_logs(value)
        super().set_key_value(self.section_name, key.name, value)


player_info_config = PlayerInfoConfig()
board_config = BoardConfig()
ui_config = UiConfig()
engine_config = EngineConfig()
lichess_config = LichessConfig()
