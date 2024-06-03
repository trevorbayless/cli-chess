from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.engine import EngineModel
    from chess.engine import PlayResult


class EnginePresenter:
    def __init__(self, model: EngineModel):
        self.model = model

    def start_engine(self) -> None:
        """Notifies the model to start the engine"""
        self.model.start_engine()

    def get_best_move(self) -> PlayResult:
        """Notify the engine to get the best move from the current position"""
        return self.model.get_best_move()

    def quit_engine(self) -> None:
        """Calls the model to notify the engine to quit"""
        self.model.quit_engine()
