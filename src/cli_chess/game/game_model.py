from cli_chess.game.board import BoardModel
from cli_chess.game.move_list import MoveListModel
from cli_chess.game.material_difference import MaterialDifferenceModel
from cli_chess.game.offline.engine import EngineModel


class GameModel:
    def __init__(self):
        self.board_model = BoardModel()
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)


class OfflineGameModel(GameModel):
    def __init__(self):
        super().__init__()
        self.engine_model = EngineModel(self.board_model)
