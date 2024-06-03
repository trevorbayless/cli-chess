from __future__ import annotations
from cli_chess.menus.program_settings_menu import ProgramSettingsMenuView
from cli_chess.menus import MultiValueMenuPresenter
from cli_chess.utils.config import TerminalConfig
from cli_chess.utils.common import COLOR_DEPTH_MAP
from cli_chess.utils.ui_common import set_color_depth
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.program_settings_menu import ProgramSettingsMenuModel


class ProgramSettingsMenuPresenter(MultiValueMenuPresenter):
    """Defines the presenter for the program settings menu"""
    def __init__(self, model: ProgramSettingsMenuModel):
        self.model = model
        self.view = ProgramSettingsMenuView(self)
        super().__init__(self.model, self.view)

    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        menu_item = self.model.get_menu_options()[selected_option]
        selected_option = menu_item.option
        selected_value = menu_item.selected_value['name']

        if selected_option == TerminalConfig.Keys.TERMINAL_COLOR_DEPTH:
            color_depth = list(COLOR_DEPTH_MAP.keys())[list(COLOR_DEPTH_MAP.values()).index(selected_value)]
            self.model.save_terminal_color_depth_setting(color_depth)
            set_color_depth(color_depth)
        else:
            self.model.save_selected_game_config_setting(selected_option, selected_value == "Yes")
