from .game_model import GameModel
from .game_view import GameView

class GamePresenter:
    """ Mediator between the GameModel and the GameView.
        Takes events from GameModel and GameView and translates
        into actions each can understand.
    """
    def __init__(self, model : GameModel):
        self.game_model = model
        self.game_view = GameView(self)
        self.initialize_view()


    def initialize_view(self):
        self.game_view.update_board_output_container(self.game_model.board.get_board_display())


    def input_received(self, input):
        self.game_model.make_move(input)
        self.game_view.update_board_output_container(self.game_model.board.get_board_display())
