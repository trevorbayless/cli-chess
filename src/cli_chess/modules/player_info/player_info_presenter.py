from __future__ import annotations
from cli_chess.modules.player_info import PlayerInfoView
from chess import Color, COLOR_NAMES
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase


class PlayerInfoPresenter:
    def __init__(self, model: GameModelBase):
        self.model = model

        orientation = self.model.board_model.get_board_orientation()
        self.view_upper = PlayerInfoView(self, self.get_player_info(not orientation))
        self.view_lower = PlayerInfoView(self, self.get_player_info(orientation))

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        if 'boardOrientationChanged' in kwargs or 'onlineGameOver' in kwargs:
            orientation = self.model.board_model.get_board_orientation()
            self.view_upper.update(self.get_player_info(not orientation))
            self.view_lower.update(self.get_player_info(orientation))

    def get_player_info(self, color: Color) -> dict:
        return self.model.game_metadata['players'][COLOR_NAMES[color]]
