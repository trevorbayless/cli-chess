import os
import configparser

#TODO: Handle exceptions

class BaseConfig:
    def __init__(self, config_file):
        '''Initialize the base class'''
        self.filename = config_file
        self.parser = configparser.SafeConfigParser()


    def read_config(self):
        '''Read in the config file from the system
           Returns True if the config file exists'''
        self.parser.read(self.filename)
        return self.config_exists()


    def write_config(self):
        '''Writes to the configuration file'''
        with open(self.filename, 'w') as config_file:
            self.parser.write(config_file)


    def config_exists(self):
        '''Checks if the default config exists'''
        return os.path.isfile(self.filename)


    def add_section(self, section_name):
        '''Add a section to the configuration file'''
        self.parser[section_name] = {}
        self.write_config()


    def set_key_value(self, section_name, key, value):
        '''Add a key to a section in the configuration file'''
        self.parser[section_name][key] = value
        self.write_config()


    def update_config_value(self, section, key, value):
        '''Update the config files section/key with the value passed in'''
        with open(self.filename, 'w') as config_file:
            self.parser[section][key] = value
            self.parser.write(config_file)


    def get_config_filename(self):
        '''Returns the configurations filename'''
        return self.filename


    def get_key_value(self, section, key, lowercase=True):
        '''Returns the value at the passed in section/key pair'''
        try:
            key_value = self.parser.get(section, key).strip()
            if lowercase:
                key_value = key_value.lower()
            return key_value
        except Exception as e:
            self.handle_exception(e)


    def get_key_boolean_value(self, section, key):
        try:
            return self.parser.getboolean(section, key)
        except Exception as e:
            self.handle_exception(e)


    def handle_exception(self, exception):
        '''Handles exceptions that occur while parsing the configuration file'''
        #TODO: Handle base class exceptions
        print("Exception caught while handling the configuration file")


class Config(BaseConfig):
    '''Class to create, update, and read from the configuration file'''
    def __init__(self, config_file):
        '''Initialize the class'''
        super().__init__(config_file)
        if not super().read_config():
            self.create_default_config()


    def create_default_config(self, overwrite=False):
        '''Creates the default configuration file'''
        if not super().config_exists() or overwrite:
            self.create_board_section()
            self.create_ui_section()
            self.create_lichess_section()


    def create_board_section(self):
        '''Creates the default 'board' section in the config file'''
        is_unix = os.name == "posix"
        super().add_section(Config.Sections.BOARD)
        self.set_board_value(Config.BoardKeys.BOARD_COLOR, "green")
        self.set_board_value(Config.BoardKeys.PIECE_NOTATION, "symbol" if is_unix else "letter")
        self.set_board_value(Config.BoardKeys.BLINDFOLD_MODE, "no")
        self.set_board_value(Config.BoardKeys.SHOW_BOARD_HIGHLIGHTS, "yes")
        self.set_board_value(Config.BoardKeys.SHOW_BOARD_COORDINATES, "yes")
        self.set_board_value(Config.BoardKeys.SHOW_MOVE_LIST, "yes")


    def set_board_value(self, key, value):
        '''Modify (or add) a BOARD key value'''
        super().set_key_value(Config.Sections.BOARD, key, value)


    def get_board_value(self, key):
        '''Returns a value from the BOARD section'''
        return super().get_key_value(Config.Sections.BOARD, key)


    def get_board_boolean(self, key):
        '''Returns a boolean value from the BOARD section'''
        return super().get_key_boolean_value(Config.Sections.BOARD, key)


    def create_ui_section(self):
        '''Creates the default 'ui' section in the config file'''
        super().add_section(Config.Sections.UI)
        self.set_ui_value(Config.UiKeys.ZEN_MODE, "no")


    def set_ui_value(self, key, value):
        '''Modify (or add) a UI key value'''
        super().set_key_value(Config.Sections.UI, key, value)


    def get_ui_value(self, key):
        '''Returns a value from the UI section'''
        return super().get_key_value(Config.Sections.UI, key)


    def get_ui_boolean(self, key):
        '''Returns a boolean value from the UI section'''
        return super().get_key_boolean_value(Config.Sections.UI, key)


    def create_lichess_section(self):
        '''Creates the default 'lichess' section in the config file'''
        super().add_section(Config.Sections.LICHESS)
        self.set_lichess_value(Config.LichessKeys.API_KEY, "")


    def set_lichess_value(self, key, value):
        '''Modify (or add) a LICHESS key value'''
        super().set_key_value(Config.Sections.LICHESS, key, value)


    def get_lichess_value(self, key):
        '''Returns a value from the LICHESS section'''
        return super().get_key_value(Config.Sections.LICHESS, key)


    def get_lichess_api_key(self):
        '''Returns the stored lichess api key'''
        api_key = super().get_key_value(Config.Sections.LICHESS, Config.LichessKeys.API_KEY, False)

        if api_key != "":
            return api_key
        else:
            return None


    def get_lichess_boolean(self, key):
        '''Returns a boolean value from the UI section'''
        return super().get_key_boolean_value(Config.Sections.LICHESS, key)


    class Sections:
        '''Holds the section names'''
        BOARD = "board"
        UI = "ui"
        LICHESS = "lichess"


    class BoardKeys:
        '''Holds the name of keys in the BOARD section'''
        BOARD_COLOR = "board_color"                       # board color
        PIECE_NOTATION = "piece_notation"                 # symbol or letter
        BLINDFOLD_MODE = "blindfold_mode"                 # invisible pieces
        SHOW_BOARD_HIGHLIGHTS = "show_board_highlights"   # last moves and check
        SHOW_BOARD_COORDINATES = "show_board_coordinates" # display A-H, 1-8
        SHOW_MOVE_LIST = "show_move_list"                 # display the move list


    class UiKeys:
        '''Holds the name of keys in the UI section'''
        ZEN_MODE = "zen_mode" # simple ui


    class LichessKeys:
        '''Holds the name of keys in the LICHESS section'''
        API_KEY = "api_key"  # lichess api key


config = Config("config.ini")
