from __future__ import annotations
from cli_chess.menus import MenuPresenter
from cli_chess.menus.online_games_menu import OnlineGamesMenuView
from cli_chess.menus.versus_menus import OnlineVsComputerMenuModel, OnlineVsRandomOpponentMenuModel, OnlineVersusMenuPresenter
from cli_chess.menus.tv_channel_menu import TVChannelMenuModel, TVChannelMenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.online_games_menu import OnlineGamesMenuModel


class OnlineGamesMenuPresenter(MenuPresenter):
    """Defines the online games menu"""
    def __init__(self, model: OnlineGamesMenuModel):
        self.model = model
        self.vs_random_opponent_menu_presenter = OnlineVersusMenuPresenter(OnlineVsRandomOpponentMenuModel(), is_vs_ai=False)
        self.vs_computer_menu_presenter = OnlineVersusMenuPresenter(OnlineVsComputerMenuModel(), is_vs_ai=True)
        self.tv_channel_menu_presenter = TVChannelMenuPresenter(TVChannelMenuModel())
        self.view = OnlineGamesMenuView(self)
        super().__init__(self.model, self.view)
