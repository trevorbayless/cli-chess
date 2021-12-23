from cli_chess.game.material_difference import material_difference_presenter
from . import GameModel, GameView
from .board import BoardModel, BoardPresenter
from .move_list import MoveListModel, MoveListPresenter
from .material_difference import MaterialDifferenceModel, MaterialDifferencePresenter
from chess import WHITE, BLACK


def play_offline() -> None:
    game_model = GameModel()
    game_presenter = GamePresenter(game_model)


class GamePresenter:
    def __init__(self, model: GameModel):
        # Create the board
        self.board_model = BoardModel()
        self.board_presenter = BoardPresenter(self.board_model)

        # Create the move list
        self.move_list_model = MoveListModel(self.board_model)
        self.move_list_presenter = MoveListPresenter(self.move_list_model)

        # Create material difference
        self.material_diff_model = MaterialDifferenceModel(self.board_model)
        self.material_diff_presenter_white = MaterialDifferencePresenter(self.material_diff_model, WHITE)
        self.material_diff_presenter_black = MaterialDifferencePresenter(self.material_diff_model, BLACK)

        # Setup for this game
        self.game_model = model
        self.game_view = GameView(self, self.board_presenter.view,
                                        self.move_list_presenter.view,
                                        self.material_diff_presenter_white.view,
                                        self.material_diff_presenter_black.view)


    def input_received(self, input):
        self.board_presenter.make_move(input)
