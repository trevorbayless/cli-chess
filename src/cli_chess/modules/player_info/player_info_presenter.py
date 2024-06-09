from __future__ import annotations
from cli_chess.modules.player_info import PlayerInfoView
from cli_chess.utils import EventTopics
from chess import Color
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase
    from cli_chess.core.game import PlayerMetadata


class PlayerInfoPresenter:
    def __init__(self, model: GameModelBase):
        self.model = model

        orientation = self.model.board_model.get_board_orientation()
        self.view_upper = PlayerInfoView(self, self.model.game_metadata.players[not orientation])
        self.view_lower = PlayerInfoView(self, self.model.game_metadata.players[orientation])

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, *args, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        if any(e in args for e in [EventTopics.GAME_START, EventTopics.GAME_END, EventTopics.BOARD_ORIENTATION_CHANGED]):
            orientation = self.model.board_model.get_board_orientation()
            self.view_upper.update(self.get_player_info(not orientation))
            self.view_lower.update(self.get_player_info(orientation))

    def get_player_info(self, color: Color) -> PlayerMetadata:
        """Returns the player metadata for the passed in color"""
        return self.model.game_metadata.players[color]
