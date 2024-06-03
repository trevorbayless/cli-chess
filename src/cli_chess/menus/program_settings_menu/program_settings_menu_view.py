from __future__ import annotations
from cli_chess.menus import MultiValueMenuView
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.program_settings_menu import ProgramSettingsMenuPresenter


class ProgramSettingsMenuView(MultiValueMenuView):
    def __init__(self, presenter: ProgramSettingsMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=40, column_width=28)
