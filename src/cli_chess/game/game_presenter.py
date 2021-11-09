from cli_chess.board import BoardModel, BoardPresenter
from cli_chess.game import GameModel, GameView

class GamePresenter:
    def __init__(self, model : GameModel, board_model : BoardModel):
        self.board_presenter = BoardPresenter(board_model)

        self.game_model = model
        self.game_view = GameView(self, self.board_presenter.get_view())


    def input_received(self, input):
        self.board_presenter.make_move(input)
