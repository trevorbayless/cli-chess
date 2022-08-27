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

from cli_chess.utils.common import is_windows_system
from cli_chess.utils.logging import log, redact_from_logs
from os import path, makedirs
from enum import Enum
import configparser

# TODO: Handle exceptions
# TODO: Handle new config options on updates (do not overwrite full config)
# TODO: Add a "force_update" to pull new values if they have been changed during runtime


def get_config_path() -> str:
    """Returns the config filepath to use based on OS"""
    file_path = "$HOME/.config/cli-chess/"

    if is_windows_system():
        file_path = "$APPDATA/cli-chess/"

    return path.expandvars(file_path)


class BaseConfig:
    def __init__(self, filename: str) -> None:
        """Default base class constructor"""
        self.file_path = get_config_path()
        self.full_filename = self.file_path + filename
        self.parser = configparser.ConfigParser()
        self.parser.read(self.full_filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        if not path.exists(self.file_path):
            makedirs(self.file_path)

        with open(self.full_filename, 'w') as config_file:
            self.parser.write(config_file)

    def config_exists(self) -> bool:
        """Returns True if the configuration file exists"""
        return path.isfile(self.full_filename)

    def add_section(self, section: str) -> None:
        """Add a section to the configuration file"""
        self.parser[section] = {}
        self.write_config()

    def has_section(self, section: str) -> bool:
        return self.parser.has_section(section)

    def set_key_value(self, section: str, key: str, value: str) -> None:
        """Set (or add) a key/value to a section in the configuration file"""
        # TODO: Raise error if section does not exist
        self.parser[section][key] = value
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
        """Returns a dictionary of all key/values at the section passed in"""
        try:
            return dict(self.parser.items(section))
        except Exception as e:
            self.handle_exception(e)

    def handle_exception(self, e: Exception) -> None:
        """Handles exceptions that occur while parsing the configuration file"""
        log.error(f"Exception caught while parsing the configuration file: {e}")


class SectionBase(BaseConfig):
    def __init__(self, filename: str, section_name: str, section_keys):
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
            super().set_key_value(self.section_name, key["name"], key["default"])

    def get_all_values(self) -> dict:
        """Returns a dictionary of all key/values in this section"""
        return dict(super().get_sections_values(self.section_name))

    def get_value(self, key) -> str:
        """Get the value of the key passed in from the configuration file"""
        return super().get_key_value(self.section_name, key["name"], False)

    def set_value(self, key: dict, value: str) -> None:
        """Set a keys value in the configuration file"""
        super().set_key_value(self.section_name, key["name"], value)

    def get_boolean(self, key: dict) -> bool:
        """Retrieve the boolean value at the passed in section/key pair"""
        return super().get_key_boolean_value(self.section_name, key["name"])


class BoardSection(SectionBase):
    """Creates and manages the "board" section of the config"""
    class Keys:
        SHOW_BOARD_COORDINATES = {"name": "show_board_coordinates", "default": "true"}
        RANK_LABEL_COLOR = {"name": "rank_label_color", "default": "gray"}
        FILE_LABEL_COLOR = {"name": "file_label_color", "default": "gray"}
        SHOW_BOARD_HIGHLIGHTS = {"name": "show_board_highlights", "default": "true"}
        LAST_MOVE_COLOR = {"name": "last_move_color", "default": "yellowgreen"}
        LIGHT_SQUARE_COLOR = {"name": "light_square_color", "default": "cadetblue"}
        DARK_SQUARE_COLOR = {"name": "dark_square_color", "default": "darkslateblue"}
        IN_CHECK_COLOR = {"name": "in_check_color", "default": "red"}
        BLINDFOLD_CHESS = {"name": "blindfold_chess", "default": "false"}
        USE_UNICODE_PIECES = {"name": "use_unicode_pieces", "default": "true" if is_windows_system() else "false"}
        LIGHT_PIECE_COLOR = {"name": "light_piece_color", "default": "white"}
        DARK_PIECE_COLOR = {"name": "dark_piece_color", "default": "black"}

        def __getitem__(self):
            test = "hi"
            return self["name"]

    def __init__(self, filename: str):
        super().__init__(filename, "board", self.Keys)


class UiSection(SectionBase):
    """Creates and manages the "ui" section of the config"""
    class Keys(Enum):
        ZEN_MODE = {"name": "zen_mode", "default": "false"}

    def __init__(self, filename: str):
        super().__init__(filename, "ui", self.Keys)


class EngineSection(SectionBase):
    """Creates and manages the "engine" section of the config"""
    class Keys:
        ENGINE_PATH = {"name": "engine_path", "default": ""}

    def __init__(self, filename: str):
        super().__init__(filename, "engine", self.Keys)


class LichessSection(SectionBase):
    """Creates and manages the "lichess" section of the config"""
    class Keys:
        API_TOKEN = {"name": "api_token", "default": ""}

    def __init__(self, filename: str):
        super().__init__(filename, "lichess", self.Keys)
        redact_from_logs(self.get_value(self.Keys.API_TOKEN))


CONFIG_FILENAME = "config.ini"
board_config = BoardSection(CONFIG_FILENAME)
ui_config = UiSection(CONFIG_FILENAME)
engine_config = EngineSection(CONFIG_FILENAME)
lichess_config = LichessSection(CONFIG_FILENAME)
