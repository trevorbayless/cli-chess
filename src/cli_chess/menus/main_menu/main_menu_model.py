from enum import Enum, auto


class MainMenuOptions(Enum):
    PLAY_OFFLINE = auto()
    SETTINGS = auto()
    ABOUT = auto()


class MainMenuModel:
    def __init__(self):
        self.options = [(MainMenuOptions.PLAY_OFFLINE, "Play offline"),
                        (MainMenuOptions.SETTINGS, "Manage settings"),
                        (MainMenuOptions.ABOUT, "About")]

    def get_menu_options(self) -> list:
        """Returns the list of main menu options"""
        return self.options
