from __future__ import annotations
from cli_chess.menus.versus_menus import VersusMenuView
from cli_chess.menus import MultiValueMenuPresenter
from cli_chess.core.game.game_options import GameOption, BaseGameOptions, OfflineGameOptions, OnlineGameOptions, OnlineDirectChallengesGameOptions
from cli_chess.core.game import start_online_game, start_offline_game
from cli_chess.utils import log
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from cli_chess.menus.versus_menus import VersusMenuModel, OfflineVsComputerMenuModel


class VersusMenuPresenter(MultiValueMenuPresenter, ABC):
    """Base presenter for the VsComputer menus"""
    def __init__(self, model: VersusMenuModel):
        self.model = model
        self.view = VersusMenuView(self)
        super().__init__(self.model, self.view)

    @abstractmethod
    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        pass

    @abstractmethod
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
            log.error(f"Error creating dictionary of selections: {e}")
            raise


class OfflineVersusMenuPresenter(VersusMenuPresenter):
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
        try:
            game_parameters = super()._create_dict_of_selected_values(OfflineGameOptions)
            start_offline_game(game_parameters)
        except Exception as e:
            log.error(e)
            raise


class OnlineVersusMenuPresenter(VersusMenuPresenter):
    """Defines the presenter for the OnlineVsComputer menu"""
    def __init__(self, model: VersusMenuModel, is_vs_ai: bool):
        self.model = model
        self.is_vs_ai = is_vs_ai
        super().__init__(self.model)

    def value_cycled_handler(self, selected_option: int):
        """A handler that's called when the value of the selected option changed"""
        pass

    def handle_start_game(self) -> None:
        """Starts the game using the currently selected menu values"""
        try:
            game_parameters = super()._create_dict_of_selected_values(OnlineGameOptions if not self.is_vs_ai else OnlineDirectChallengesGameOptions)
            start_online_game(game_parameters, is_vs_ai=self.is_vs_ai)
        except Exception as e:
            log.error(e)
            raise
