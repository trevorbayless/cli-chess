from chess import variant
from . import GameModel, GameView
from .board import BoardModel, BoardPresenter
from .move_list import MoveListModel, MoveListPresenter


class GamePresenter:
    def __init__(self, model : GameModel):
        # Create the board
        self.board_model = BoardModel()
        self.board_presenter = BoardPresenter(self.board_model)

        # Create the move list
        self.move_list_model = MoveListModel(self.board_model)
        self.move_list_presenter = MoveListPresenter(self.move_list_model)

        self.game_model = model
        self.game_view = GameView(self, self.board_presenter.get_view(),
                                        self.move_list_presenter.get_view())


    def input_received(self, input):
        self.board_presenter.make_move(input)
        self.move_list_presenter.update_move_list()
