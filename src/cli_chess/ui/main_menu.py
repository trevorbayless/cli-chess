from enum import Enum
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Dialog, Label, RadioList, Button, ValidationToolbar
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.application import get_app
from cli_chess.ui.about import show_about

from cli_chess.game.game_view import GameView


def show_main_menu() -> None:
    """Sets the app layout to the Main Menu"""
    menu = MainMenu()
    get_app().layout = Layout(menu, menu.menu_list)


def play_online() -> None:
    view = GameView()
    get_app().layout = Layout(view)


class MainMenuOptions(Enum):
    PLAY_ONLINE = 0
    PLAY_OFFLINE = 1
    WATCH_TV = 2
    SETTINGS = 3
    ABOUT = 4


menu_map = {
    MainMenuOptions.PLAY_ONLINE: play_online,
    MainMenuOptions.PLAY_OFFLINE: None,
    MainMenuOptions.WATCH_TV: None,
    MainMenuOptions.SETTINGS: None,
    MainMenuOptions.ABOUT: show_about
}

class MainMenu:
    """Defines the Main Menu"""
    def __init__(self):
        self.menu_list = RadioList(self.get_menu_options())
        self.ok_button = Button(text="Ok", handler=self.ok_handler)
        self.quit_button = Button(text="Quit", handler=self.quit_handler)
        self.dialog = self.create_dialog()


    def get_menu_options(self) -> list:
        """Return the main menu options"""
        options = [(MainMenuOptions.PLAY_ONLINE, "Play online"),
                   (MainMenuOptions.PLAY_OFFLINE, "Play offline"),
                   (MainMenuOptions.WATCH_TV, "Watch Lichess TV"),
                   (MainMenuOptions.SETTINGS, "Manage settings"),
                   (MainMenuOptions.ABOUT, "About")]
        return options


    def create_dialog(self) -> Dialog:
        """Create the main dialog"""
        return Dialog(title=HTML("Welcome to cli-chess!"),
                      body=HSplit(
                           [Label(text="What would you like to do?", dont_extend_height=True), self.menu_list],
                           padding=1),
                      buttons=[ self.ok_button, self.quit_button ],
                      with_background=True)


    def ok_handler(self) -> None:
        """Handler for the 'Ok' button"""
        menu_map[self.menu_list.current_value]()


    def quit_handler(self) -> None:
        """Handler for the 'Quit' button"""
        get_app().exit()


    def __pt_container__(self) -> Dialog:
        """Returns the dialog for container use"""
        return self.dialog


# def watch_tv():
#     try:
#         client = initialize_api_client()
#         pprint(client.games.get_tv_channels())
#     except Exception as e:
#         print(e)
#         run()


# def play_online():
#     try:
#         client = initialize_api_client()
#         event_manager = initialize_event_manager(client)

#         #TODO: Show a menu here of playing a game in progress, challenge, seek

#         print("Your games:")
#         ongoing_games = client.games.get_ongoing()
#         for game in ongoing_games:
#             print(game['gameId'] + "\n")

#         game_id = prompt("ID of game to play: ")
#         game_found = False
#         for my_games in event_manager.get_active_games():
#             if game_id == my_games['game']['id']:
#                 print(f"Listening to game: {game_id}")
#                 game_stream = GameManager(client, game_id)
#                 game_stream.start()
#                 game_found = True
#                 break

#         if not game_found:
#             print("Invalid game id")

#     except Exception as e:
#         print(e)
#         run()


# def play_offline():
#     #TODO: Prompt user for defaults

#     board = Board() # Using default params
#     board.print_board()

#     game_in_progress = True
#     while game_in_progress:
#         user_move = ""
#         try:
#             user_move = prompt("Make a move: ")
#         except:
#             game_in_progress = False
#             break
#         try:
#             board.make_move(user_move)
#             common_utils.clear_screen()
#             board.print_board()
#         except Exception as e:
#             print(e)

#         if board.is_game_over():
#             game_in_progress = False
#             print(board.game_result())


# def initialize_api_client():
#     """Returns and initializes the API client"""
#     proceed = False

#     if common_utils.is_valid_lichess_token(config.get_lichess_value(config.LichessKeys.API_TOKEN, lowercase=False)):
#         proceed = True
#     else:
#         pass
#         # SHOW REQUEST TO GENERATE API TOKEN ##proceed = prompts.show_request_to_generate_token()

#     if proceed:
#         api_token = config.get_lichess_value(config.LichessKeys.API_TOKEN, lowercase=False)
#         session = berserk.TokenSession(api_token)
#         client = berserk.Client(session)

#         account = client.account.get()
#         config.set_lichess_value(config.LichessKeys.USERNAME, account['username'])

#         return client
#     else:
#         raise ValueError


# def initialize_event_manager(client):
#     """Initializes IncomingEventManager to start listening for incoming events."""
#     event_manager = IncomingEventManager(client)
#     event_manager.daemon = True  # Daemon thread will not block interpereter from exiting
#     event_manager.start()

#     return event_manager
