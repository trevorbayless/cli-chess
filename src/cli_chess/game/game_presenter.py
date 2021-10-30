from .game_model import GameModel

class GamePresenter:
    """ Mediator between the GameModel and the GameView.
        Takes events from GameModel and GameView and translates
        into actions each can understand.
    """
    def __init__(self):
        self.game_model = GameModel()


    def get_board_output(self) -> str:
        return self.game_model.board.get_board_display()


    def receive_input(self, input):
        self.game_model.make_move(input)
