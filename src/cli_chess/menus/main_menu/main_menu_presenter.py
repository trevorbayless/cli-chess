from .main_menu_model import MainMenuModel, MainMenuOptions
from .main_menu_view import MainMenuView
from cli_chess.game import play_offline
from cli_chess.dialogs.about import show_about


menu_map = {
    MainMenuOptions.PLAY_OFFLINE: play_offline,
    MainMenuOptions.SETTINGS: None,
    MainMenuOptions.ABOUT: show_about
}


class MainMenuPresenter:
    """Defines the Main Menu"""
    def __init__(self):
        self.model = MainMenuModel()
        self.view = MainMenuView(self)


    def get_menu_options(self) -> list:
        """Return the main menu options"""
        return self.model.get_menu_options()


    def ok_handler(self) -> None:
        """Handler for the 'Ok' button"""
        menu_map[self.view.get_selected_option()]()

