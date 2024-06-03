from __future__ import annotations
from cli_chess.menus import MenuPresenter
from cli_chess.menus.main_menu import MainMenuView
from cli_chess.menus.online_games_menu import OnlineGamesMenuModel, OnlineGamesMenuPresenter
from cli_chess.menus.offline_games_menu import OfflineGamesMenuModel, OfflineGamesMenuPresenter
from cli_chess.menus.settings_menu import SettingsMenuModel, SettingsMenuPresenter
from cli_chess.modules.about import AboutPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.main_menu import MainMenuModel


class MainMenuPresenter(MenuPresenter):
    """Defines the Main Menu"""
    def __init__(self, model: MainMenuModel):
        self.model = model
        self.online_games_menu_presenter = OnlineGamesMenuPresenter(OnlineGamesMenuModel())
        self.offline_games_menu_presenter = OfflineGamesMenuPresenter(OfflineGamesMenuModel())
        self.settings_menu_presenter = SettingsMenuPresenter(SettingsMenuModel())
        self.about_presenter = AboutPresenter()
        self.view = MainMenuView(self)
        self.selection = self.model.get_menu_options()[0].option

        super().__init__(self.model, self.view)
