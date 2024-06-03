from cli_chess.utils.common import is_linux_os, is_windows_os
from cli_chess.utils.logging import log, redact_from_logs
from cli_chess.utils.event import Event
from cli_chess.utils.common import VALID_COLOR_DEPTHS
from getpass import getuser
from enum import Enum
import configparser
import os
from typing import List

all_configs: List["SectionBase"] = []
DEFAULT_CONFIG_FILENAME = "config.ini"


def get_config_path() -> str:
    """Returns the config filepath to use based on OS"""
    file_path = "$HOME/.config/cli-chess/"

    if is_windows_os():
        file_path = "$APPDATA/cli-chess/"

    return os.path.expandvars(file_path)


def force_recreate_configs() -> None:
    """Forces a clean recreation of all configs"""
    # Handle deletion first as configs can exist in the same file
    # and we don't want to delete a newly created config/section
    for config in all_configs:
        if os.path.exists(config.full_filename):
            os.remove(config.full_filename)

    # second loop to handle recreation
    for config in all_configs:
        config.parser = config._get_parser() # noqa
        config.create_section()


def print_program_config() -> None:
    """Prints the configuration files for debugging purposes"""
    filenames = []  # Keep track of filenames printed so it's not duplicated
    api_token = lichess_config.get_value(lichess_config.Keys.API_TOKEN).strip()
    for config in all_configs:
        if config.full_filename not in filenames:
            filenames.append(config.full_filename)
            try:
                with open(config.full_filename, 'r') as config_file:
                    config_output = config_file.read()
                    if api_token:
                        config_output = config_output.replace(api_token, "**REDACTED**")

                    print(config_output)
            except OSError as e:
                print(e)


class BaseConfig:
    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME) -> None:
        """Default base class constructor"""
        self.file_path = get_config_path()
        self.full_filename = self.file_path + filename
        self.parser = self._get_parser()

        # Event called on any configuration write event (across sections)
        self.e_config_updated = Event()

    def _get_parser(self) -> "ConfigParser":  # noqa: F821
        """Returns the config parser object"""
        parser = configparser.ConfigParser()
        parser.read(self.full_filename)
        return parser

    def write_config(self) -> None:
        """Writes to the configuration file"""
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        with open(self.full_filename, 'w') as config_file:
            self.parser.write(config_file)
            self.e_config_updated.notify()

    def config_exists(self) -> bool:
        """Returns True if the configuration file exists"""
        return os.path.isfile(self.full_filename)

    def add_section(self, section: str) -> None:
        """Add a section to the configuration file"""
        self.parser[section] = {}
        self.write_config()

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

        # Keep track of all config sections (used on recreation)
        all_configs.append(self)

    def _verify_section_integrity(self):
        """Verifies a config sections integrity by validating the section exists as well
           as all expected keys. If the section is missing, the entire section is recreated.
           If a key is missing from the section, the key will be re-added with its default value.
        """
        if self._section_exists():
            for key in self.section_keys:
                if not self._section_has_key(key):
                    super().set_key_value(self.section_name, key.name, key.default_value)
        else:
            self.create_section()

    def create_section(self) -> None:
        """Creates this section using key value defaults"""
        super().add_section(self.section_name)
        for key in self.section_keys:
            super().set_key_value(self.section_name, key.name, key.default_value)

    def get_all_values(self) -> dict:
        """Returns a dictionary of all key/values in this section.
           The returned result is a raw text based dictionary.
        """
        return super().get_sections_values(self.section_name)

    def get_value(self, key: Enum) -> str:
        """Get the value of the key passed in from the configuration file"""
        return super().get_key_value(self.section_name, key.name, False)

    def set_value(self, key: Enum, value: str) -> None:
        """Set a keys value in the configuration file"""
        super().set_key_value(self.section_name, key.name, value)

    def get_boolean(self, key: Enum) -> bool:
        """Retrieve the boolean value at the passed in section/key pair"""
        return super().get_key_boolean_value(self.section_name, key.name)

    def _section_exists(self) -> bool:
        """Returns true if this section exists in the configuration file"""
        return self.parser.has_section(self.section_name)

    def _section_has_key(self, key: Enum) -> bool:
        """Returns true if the passed in key exists in the supplied section"""
        return self.parser.has_option(self.section_name, key.name)


class PlayerInfoConfig(SectionBase):
    """Creates and manages the "player info" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        OFFLINE_PLAYER_NAME = "offline_player_name"

        @property
        def default_value(self):
            """Returns the default value for the key"""
            default_lookup = {
                self.OFFLINE_PLAYER_NAME: getuser() if getuser() else "You"
            }
            return default_lookup[self]

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_player_info_config_updated = Event()
        super().__init__(section_name="player_info", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_player_info_config_updated.notify()


class GameConfig(SectionBase):
    """Creates and manages the "game" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        SHOW_BOARD_COORDINATES = "show_board_coordinates"
        SHOW_BOARD_HIGHLIGHTS = "show_board_highlights"
        BLINDFOLD_CHESS = "blindfold_chess"
        USE_UNICODE_PIECES = "use_unicode_pieces"
        SHOW_MOVE_LIST_IN_UNICODE = "show_move_list_in_unicode"
        SHOW_MATERIAL_DIFF_IN_UNICODE = "show_material_diff_in_unicode"
        PAD_UNICODE = "pad_unicode"

        @property
        def default_value(self):
            """Returns the default value for the key"""
            default_lookup = {
                self.SHOW_BOARD_COORDINATES: True,
                self.SHOW_BOARD_HIGHLIGHTS: True,
                self.BLINDFOLD_CHESS: False,
                self.USE_UNICODE_PIECES: True,
                self.SHOW_MOVE_LIST_IN_UNICODE: False,
                self.SHOW_MATERIAL_DIFF_IN_UNICODE: True,
                self.PAD_UNICODE: True,
            }
            return default_lookup[self]

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_game_config_updated = Event()
        super().__init__(section_name="game", section_keys=self.Keys, filename=filename)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_game_config_updated.notify()

    def get_all_values(self) -> dict:
        """Returns a dictionary of all key/values in this section.
           The keys of the dictionary is this sections Key enum.
        """
        raw_config_values = super().get_all_values()
        enum_mapped_dict = raw_config_values.copy()
        for key in raw_config_values:
            try:
                enum_mapped_dict[GameConfig.Keys(key)] = enum_mapped_dict.pop(key)
            except ValueError:
                log.error(f"Unrecognized key ({key}) found in configuration")
        return enum_mapped_dict


class TerminalConfig(SectionBase):
    """Creates and manages the "terminal" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        TERMINAL_COLOR_DEPTH = "terminal_color_depth"

        @property
        def default_value(self):
            """Returns the default value for the key"""
            default_lookup = {
                self.TERMINAL_COLOR_DEPTH: "DEPTH_24_BIT" if is_linux_os() else "DEPTH_8_BIT"
            }
            return default_lookup[self]

    def __init__(self, filename: str = DEFAULT_CONFIG_FILENAME):
        self.e_program_config_updated = Event()
        super().__init__(section_name="terminal", section_keys=self.Keys, filename=filename)

    def get_value(self, key: Enum) -> str:
        """Get the value of the key passed in from the configuration file"""
        value = super().get_key_value(self.section_name, key.name, False)
        if key == self.Keys.TERMINAL_COLOR_DEPTH and value not in VALID_COLOR_DEPTHS:
            super().set_value(self.Keys.TERMINAL_COLOR_DEPTH, self.Keys.TERMINAL_COLOR_DEPTH.default_value)
        return super().get_key_value(self.section_name, key.name, False)

    def write_config(self) -> None:
        """Writes to the configuration file"""
        super().write_config()
        self.e_program_config_updated.notify()


class LichessConfig(SectionBase):
    """Creates and manages the "lichess" configuration. This configuration can
       either live in its own file, or be appended as a section by using a
       configuration filename that already exists (such as DEFAULT_CONFIG_FILENAME).
       By default, this will be appended to the default configuration.
    """
    class Keys(Enum):
        API_TOKEN = "api_token"

        @property
        def default_value(self):
            """Returns the default value for the key"""
            default_lookup = {
                self.API_TOKEN: ""
            }
            return default_lookup[self]

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
game_config = GameConfig()
terminal_config = TerminalConfig()
lichess_config = LichessConfig()
