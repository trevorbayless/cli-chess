from . import EngineModel


class EnginePresenter:
    def __init__(self, engine_model: EngineModel):
        self.engine_model = engine_model


    async def get_best_move(self) -> str:
        return await self.engine_model.get_best_move()
