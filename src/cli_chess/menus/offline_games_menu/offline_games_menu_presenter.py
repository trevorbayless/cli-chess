from __future__ import annotations
from cli_chess.menus.offline_games_menu import OfflineGamesMenuView
from cli_chess.menus.versus_menus import OfflineVsComputerMenuModel, OfflineVersusMenuPresenter
from cli_chess.menus import MenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.offline_games_menu import OfflineGamesMenuModel


class OfflineGamesMenuPresenter(MenuPresenter):
    def __init__(self, model: OfflineGamesMenuModel):
        self.model = model
        self.vs_computer_menu_presenter = OfflineVersusMenuPresenter(OfflineVsComputerMenuModel())
        self.view = OfflineGamesMenuView(self)
        self.selection = self.model.get_menu_options()[0].option

        super().__init__(self.model, self.view)
