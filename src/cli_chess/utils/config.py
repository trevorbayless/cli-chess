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

from os import path, makedirs
import configparser
from cli_chess.utils import is_windows_system

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

    def read_config(self) -> bool:
        """Attempts to read the configuration file (True if file exists)"""
        self.parser.read(self.full_filename)
        return self.config_exists()

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

    def handle_exception(self, e: Exception) -> None:
        """Handles exceptions that occur while parsing the configuration file"""
        # TODO: Handle base class exceptions
        print("Exception caught while handling the configuration file. Please recreate the configuration file.")


class Config(BaseConfig):
    """Class to create, update, and read from the configuration file"""
    def __init__(self, filename: str) -> None:
        """Default constructor. Calls the base class to read the configuration
           file. If the file does not exist, the default configuration is created.
        """
        super().__init__(filename)
        if not super().read_config():
            self.create_default_config()

    def create_default_config(self, overwrite: bool = False) -> None:
        """Creates the default configuration file"""
        if not super().config_exists() or overwrite:
            self.create_board_section()
            self.create_ui_section()
            self.create_engine_section()
            self.create_lichess_section()

    def create_board_section(self) -> None:
        """Creates the default 'BOARD' section in the config file"""
        super().add_section(Config.Sections.BOARD)
        self.set_board_value(Config.BoardKeys.SHOW_BOARD_COORDINATES, "yes")
        self.set_board_value(Config.BoardKeys.RANK_LABEL_COLOR, "gray")
        self.set_board_value(Config.BoardKeys.FILE_LABEL_COLOR, "gray")
        self.set_board_value(Config.BoardKeys.SHOW_BOARD_HIGHLIGHTS, "yes")
        self.set_board_value(Config.BoardKeys.LAST_MOVE_COLOR, "yellowgreen")
        self.set_board_value(Config.BoardKeys.LIGHT_SQUARE_COLOR, "cadetblue")
        self.set_board_value(Config.BoardKeys.DARK_SQUARE_COLOR, "darkslateblue")
        self.set_board_value(Config.BoardKeys.IN_CHECK_COLOR, "red")
        self.set_board_value(Config.BoardKeys.BLINDFOLD_CHESS, "no")
        self.set_board_value(Config.BoardKeys.USE_UNICODE_PIECES, "no" if is_windows_system() else "yes")
        self.set_board_value(Config.BoardKeys.LIGHT_PIECE_COLOR, "white")
        self.set_board_value(Config.BoardKeys.DARK_PIECE_COLOR, "black")

    def set_board_value(self, key: str, value: str) -> None:
        """Modify (or add) a keys value at the 'BOARD' section"""
        super().set_key_value(Config.Sections.BOARD, key, value)

    def get_board_value(self, key: str, lowercase: bool = True) -> str:
        """Returns a value from the 'BOARD' section at the passed in key"""
        return super().get_key_value(Config.Sections.BOARD, key, lowercase)

    def get_board_boolean(self, key: str) -> bool:
        """Returns a boolean value from the 'BOARD' section at the passed in key"""
        return super().get_key_boolean_value(Config.Sections.BOARD, key)

    def create_ui_section(self) -> None:
        """Creates the default 'UI' section in the config file"""
        super().add_section(Config.Sections.UI)
        self.set_ui_value(Config.UiKeys.ZEN_MODE, "no")

    def set_ui_value(self, key: str, value: str) -> None:
        """Modify (or add) a keys value at the 'UI' section"""
        super().set_key_value(Config.Sections.UI, key, value)

    def get_ui_value(self, key: str, lowercase: bool = True) -> str:
        """Returns a value from the 'UI' section at the passed in key"""
        return super().get_key_value(Config.Sections.UI, key, lowercase)

    def get_ui_boolean(self, key: str) -> bool:
        """Returns a boolean value from the 'UI' section at the passed in key"""
        return super().get_key_boolean_value(Config.Sections.UI, key)

    def create_engine_section(self) -> None:
        """Creates the default 'ENGINE' section in the config file"""
        super().add_section(Config.Sections.ENGINE)
        self.set_engine_value(Config.EngineKeys.ENGINE_PATH, "")

    def set_engine_value(self, key: str, value: str) -> None:
        """Modify (or add) a keys value at the 'ENGINE' section at the passed in key"""
        super().set_key_value(Config.Sections.ENGINE, key, value)

    def get_engine_value(self, key: str) -> str:
        """Returns a value from the 'ENGINE' section at the passed in key"""
        return super().get_key_value(Config.Sections.ENGINE, key, False)

    def create_lichess_section(self) -> None:
        """Creates the default 'LICHESS' section in the config file"""
        super().add_section(Config.Sections.LICHESS)
        self.set_lichess_value(Config.LichessKeys.API_TOKEN, "")
        self.set_lichess_value(Config.LichessKeys.USERNAME, "")

    def set_lichess_value(self, key: str, value: str) -> None:
        """Modify (or add) a keys value at the 'LICHESS' section at the passed in key"""
        super().set_key_value(Config.Sections.LICHESS, key, value)

    def get_lichess_value(self, key: str, lowercase: bool = True) -> str:
        """Returns a value from the 'LICHESS' section at the passed in key"""
        return super().get_key_value(Config.Sections.LICHESS, key, lowercase)

    def get_lichess_boolean(self, key: str) -> bool:
        """Returns a boolean value from the UI section at the passed in key"""
        return super().get_key_boolean_value(Config.Sections.LICHESS, key)

    class Sections:
        """Holds the section names"""
        BOARD = "board"
        UI = "ui"
        ENGINE = "engine"
        LICHESS = "lichess"

    class BoardKeys:
        """Holds the name of keys in the BOARD section"""
        SHOW_BOARD_COORDINATES = "show_board_coordinates"  # display A-H, 1-8 labels
        RANK_LABEL_COLOR = "rank_label_color"              # color to display rank labels
        FILE_LABEL_COLOR = "file_label_color"              # color to display file labels
        SHOW_BOARD_HIGHLIGHTS = "show_board_highlights"    # last move and check
        LAST_MOVE_COLOR = "last_move_color"                # color to use to indicate the last move
        LIGHT_SQUARE_COLOR = "light_square_color"          # color to use for light squares
        DARK_SQUARE_COLOR = "dark_square_color"            # color to use for dark squares
        IN_CHECK_COLOR = "in_check_color"                  # color to highlight the king in check square
        BLINDFOLD_CHESS = "blindfold_chess"                # pieces are not shown
        USE_UNICODE_PIECES = "use_unicode_pieces"          # use unicode pieces instead of symbols
        LIGHT_PIECE_COLOR = "light_piece_color"            # color to use for light pieces
        DARK_PIECE_COLOR = "dark_piece_color"              # color to use for dark pieces

    class UiKeys:
        """Holds the name of keys in the UI section"""
        ZEN_MODE = "zen_mode"  # simple ui

    class EngineKeys:
        """Holds the name of keys in the ENGINE section"""
        ENGINE_PATH = "engine_path"

    class LichessKeys:
        """Holds the name of keys in the LICHESS section"""
        API_TOKEN = "api_token"  # lichess api token
        USERNAME = "username"    # lichess username


config = Config("config.ini")
