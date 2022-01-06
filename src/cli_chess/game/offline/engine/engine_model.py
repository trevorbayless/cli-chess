from cli_chess.game.board import BoardModel
from cli_chess.utils import config
import chess.engine


class EngineModel:
    def __init__(self, board_model: BoardModel):
        self.board_model = board_model
        self.engine_settings = {
            'engine_path': config.get_engine_value(config.EngineKeys.ENGINE_PATH),
            'think_time': 1.0
        }


    async def get_best_move(self):
        if self.engine_settings['engine_path']:
            _, engine = await chess.engine.popen_uci(self.engine_settings['engine_path'])

            return await engine.play(self.board_model.board,
                                     chess.engine.Limit(time=self.engine_settings['think_time']))
