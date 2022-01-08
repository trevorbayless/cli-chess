from . import EngineModel
from chess.engine import PlayResult


class EnginePresenter:
    def __init__(self, engine_model: EngineModel):
        self.engine_model = engine_model

    async def get_best_move(self) -> PlayResult:
        return await self.engine_model.get_best_move()
