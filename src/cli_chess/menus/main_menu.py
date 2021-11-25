from cli_chess.dialogs.about import show_about
from cli_chess.game.board import BoardModel, BoardPresenter
from cli_chess.game import GameModel, GamePresenter
from enum import Enum
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, Label, RadioList, Button, Box
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import Container, HSplit, VSplit
from prompt_toolkit.application import get_app


def play_offline() -> None:
    board_model = BoardModel()
    game_model = GameModel()
    game_presenter = GamePresenter(game_model, board_model)


def play_online() -> None:
    pass


class MainMenuOptions(Enum):
    PLAY_ONLINE = 0
    PLAY_OFFLINE = 1
    SETTINGS = 3
    ABOUT = 4


menu_map = {
    MainMenuOptions.PLAY_OFFLINE: play_offline,
    MainMenuOptions.PLAY_ONLINE: play_online,
    MainMenuOptions.SETTINGS: None,
    MainMenuOptions.ABOUT: show_about
}


class MainMenu:
    """Defines the Main Menu"""
    def __init__(self):
        self.menu_list = RadioList(self.get_menu_options())
        self.ok_button = Button(text="Ok", handler=self.ok_handler)
        self.quit_button = Button(text="Quit", handler=self.quit_handler)
        self.container = self.create_container()
        get_app().layout = Layout(self.container, self.menu_list)


    def get_menu_options(self) -> list:
        """Return the main menu options"""
        options = [(MainMenuOptions.PLAY_OFFLINE, "Play offline"),
                   (MainMenuOptions.PLAY_ONLINE, "Play online"),
                   (MainMenuOptions.SETTINGS, "Manage settings"),
                   (MainMenuOptions.ABOUT, "About")]
        return options


    def create_container(self) -> Container:
        """Create the main dialog"""
        return Box(Frame(title=HTML("Welcome to cli-chess!"),
                     body=HSplit([
                            Label(text="What would you like to do?"),
                            self.menu_list,
                            VSplit([self.ok_button, self.quit_button])])))


    def ok_handler(self) -> None:
        """Handler for the 'Ok' button"""
        menu_map[self.menu_list.current_value]()


    def quit_handler(self) -> None:
        """Handler for the 'Quit' button"""
        get_app().exit()


    def __pt_container__(self) -> Container:
        """Returns the main menu container"""
        return self.container
