from cli_chess.game.game_model import GameModel
from cli_chess.event_handler import Observer, Event


class GamePresenter(Observer):
    """ Mediator between the GameModel and the GameView.
        Takes events from GameModel and GameView and translates
        into actions each can understand.
    """
    def __init__(self, view):
        Observer.__init__(self)
        self.game_view = view
        self.game_model = GameModel()


    def make_move(self):
        move = self.game_view.get_move_input_text()
        status = self.game_model.make_move(move)
        self.game_view.set_status_text(status)
