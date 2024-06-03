from __future__ import annotations
from cli_chess.menus import MenuPresenter
from cli_chess.menus.settings_menu import SettingsMenuView
from cli_chess.menus.program_settings_menu import ProgramSettingsMenuModel, ProgramSettingsMenuPresenter
from cli_chess.modules.token_manager import TokenManagerPresenter
from cli_chess.modules.token_manager.token_manager_model import g_token_manager_model
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.settings_menu import SettingsMenuModel


class SettingsMenuPresenter(MenuPresenter):
    """Defines the settings menu"""
    def __init__(self, model: SettingsMenuModel):
        self.model = model
        self.token_manger_presenter = TokenManagerPresenter(g_token_manager_model)
        self.program_settings_menu_presenter = ProgramSettingsMenuPresenter(ProgramSettingsMenuModel())
        self.view = SettingsMenuView(self)
        super().__init__(self.model, self.view)
