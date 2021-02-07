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
      self.config[Config.Sections.BOARD]['board_color'] = 'default'                                 # board color
      self.config[Config.Sections.BOARD]['blindfold_mode'] = 'no'                                   # invisible pieces
      self.config[Config.Sections.BOARD]['show_board_highlights'] = 'yes'                           # last moves and check
      self.config[Config.Sections.BOARD]['show_board_coordinates'] = 'yes'                          # display A-H, 1-8
      self.config[Config.Sections.BOARD]['move_notation_style'] = 'symbol' if is_unix else 'letter' # symbol or letter

      self.config[Config.Sections.UI] = {}
      self.config[Config.Sections.UI]['zen_mode'] = 'no' # simple ui

      self.config[Config.Sections.LICHESS] = {}
      self.config[Config.Sections.LICHESS]['api_key'] = '' # lichess api key
      
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
    
    return self.config.get(section, key)

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
    '''Class which holds the sections in the config file'''
    BOARD = 'board'
    UI = 'ui'
    LICHESS = 'lichess'