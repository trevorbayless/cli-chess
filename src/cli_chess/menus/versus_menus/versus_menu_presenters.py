# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
from cli_chess.menus.versus_menus import VsComputerMenuView
from cli_chess.menus import MultiValueMenuPresenter
from cli_chess.modules.game_options import BaseGameOptions, OnlineGameOptions, OfflineGameOptions, GameOption
from cli_chess.core.game import start_online_game_vs_ai, start_offline_game
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from cli_chess.menus.versus_menus import VsComputerMenuModel, OnlineVsComputerMenuModel, OfflineVsComputerMenuModel


class VsComputerMenuPresenter(MultiValueMenuPresenter):
    """Base presenter for the VsComputer menus"""
    def __init__(self, model: VsComputerMenuModel):
        self.model = model
        self.view = VsComputerMenuView(self)
        super().__init__(self.model, self.view)

    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        pass

    def handle_start_game(self) -> None:
        """Starts the game using the currently selected menu values"""
        pass

    def _create_dict_of_selected_values(self, game_options_cls: Type[BaseGameOptions]) -> dict:
        """Creates a dictionary of all selected values. Raises an Exception on failure."""
        try:
            selections_dict = {}
            for index, menu_option in enumerate(self.get_visible_menu_options()):
                selections_dict[menu_option.option] = menu_option.selected_value['name']

            return game_options_cls().create_game_parameters_dict(selections_dict)
        except Exception as e:
            raise e


class OnlineVsComputerMenuPresenter(VsComputerMenuPresenter):
    """Defines the presenter for the OnlineVsComputer menu"""
    def __init__(self, model: OnlineVsComputerMenuModel):
        self.model = model
        super().__init__(self.model)

    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        pass

    def handle_start_game(self) -> None:
        """Starts the game using the currently selected menu values"""
        game_parameters = super()._create_dict_of_selected_values(OnlineGameOptions)
        start_online_game_vs_ai(game_parameters)


class OfflineVsComputerMenuPresenter(VsComputerMenuPresenter):
    """Defines the presenter for the OfflineVsComputer menu"""
    def __init__(self, model: OfflineVsComputerMenuModel):
        self.model = model
        super().__init__(self.model)

    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        menu_item = self.model.get_menu_options()[selected_option]
        selected_option = menu_item.option
        selected_value = menu_item.selected_value['name']

        if selected_option == GameOption.SPECIFY_ELO:
            self.model.show_elo_selection_option(selected_value == "Yes")

    def handle_start_game(self) -> None:
        """Starts the game using the currently selected menu values"""
        game_parameters = super()._create_dict_of_selected_values(OfflineGameOptions)
        start_offline_game(game_parameters)
