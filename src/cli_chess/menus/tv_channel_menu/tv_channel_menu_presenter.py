from __future__ import annotations
from cli_chess.menus import MenuPresenter
from cli_chess.menus.tv_channel_menu import TVChannelMenuView
from cli_chess.core.game.online_game.watch_tv import start_watching_tv
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.tv_channel_menu import TVChannelMenuModel


class TVChannelMenuPresenter(MenuPresenter):
    def __init__(self, model: TVChannelMenuModel):
        self.model = model
        self.view = TVChannelMenuView(self)

        super().__init__(self.model, self.view)

    def handle_start_watching_tv(self) -> None:
        """Changes the view to start watching tv"""
        start_watching_tv(self.selection)
