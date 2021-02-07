import configparser
import os

class Config:
  '''Class to manage and read from the config file'''

  def __init__(self, config_file):
    '''Initialize the class'''
    self.CONFIG_FILE = config_file
    self.config = configparser.ConfigParser()
    self.read_config()

  def config_exists(self):
    '''Checks if the default config exists'''
    return os.path.isfile(self.CONFIG_FILE)

  def create_default_config(self, overwrite=False):
    '''Creates the default configuration file'''
    if not self.config_exists() or overwrite:
      is_unix = os.name == "posix"

      self.config[Config.Sections.BOARD] = {}
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.BOARD_COLOR] = 'default'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.PIECE_NOTATION] = 'symbol' if is_unix else 'letter'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.LIGHT_PIECE_COLOR] = 'white'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.DARK_PIECE_COLOR] = 'black'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.BLINDFOLD_MODE] = 'no'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.SHOW_BOARD_HIGHLIGHTS] = 'yes'
      self.config[Config.Sections.BOARD][Config.Sections.BoardKeys.SHOW_BOARD_COORDINATES] = 'yes'

      self.config[Config.Sections.UI] = {}
      self.config[Config.Sections.UI][Config.Sections.UiKeys.ZEN_MODE] = 'no'

      self.config[Config.Sections.LICHESS] = {}
      self.config[Config.Sections.LICHESS][Config.Sections.LichessKeys.API_KEY] = ''
      
      with open(self.CONFIG_FILE, 'w') as config_file:
        self.config.write(config_file)

  def read_config(self):
    '''Read in the config file from the system'''
    if self.config_exists():
      self.config.read(self.CONFIG_FILE)
    else:
      self.create_default_config()

  def get_config_value(self, section, key):
    '''Returns the value in the config file as a string at the section/key'''
    if not self.config_exists():
      self.create_default_config()
    
    return self.config.get(section, key).strip()

  def get_boolean_config_value(self, section, key):
    '''Returns the value in the config file as a boolean at the section/key.
       This should only be used on known boolean values in the config file.
    '''
    if not self.config_exists():
      self.create_default_config()
    
    return self.config.getboolean(section, key)

  def update_config_value(self, section, key, value):
    '''Update the config files section/key with the value passed in'''
    if not self.config_exists():
      self.create_default_config()

    with open(self.CONFIG_FILE, 'w') as config_file:
      self.config[section][key] = value
      self.config.write(config_file)

  class Sections:
    BOARD = 'board'
    UI = 'ui'
    LICHESS = 'lichess'

    class BoardKeys:
      '''Holds the board section keys'''
      BOARD_COLOR = 'board_color'                       # board color
      PIECE_NOTATION = 'piece_notation'                 # symbol or letter
      LIGHT_PIECE_COLOR = 'light_piece_color'           # light piece color
      DARK_PIECE_COLOR = 'dark_piece_color'             # dark piece color
      BLINDFOLD_MODE = 'blindfold_mode'                 # invisible pieces
      SHOW_BOARD_HIGHLIGHTS = 'show_board_highlights'   # last moves and check
      SHOW_BOARD_COORDINATES = 'show_board_coordinates' # display A-H, 1-8

    class UiKeys:
      '''Holds the ui section keys'''
      ZEN_MODE = 'zen_mode' # simple ui

    class LichessKeys:
      '''Holds the lichess section keys'''
      API_KEY = 'api_key'  # lichess api key
