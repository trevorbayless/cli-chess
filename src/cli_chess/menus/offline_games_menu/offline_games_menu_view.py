from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.menus.offline_games_menu import OfflineGamesMenuOptions
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, HSplit
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.widgets import Box
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import ConditionalKeyBindings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.offline_games_menu import OfflineGamesMenuPresenter


class OfflineGamesMenuView(MenuView):
    def __init__(self, presenter: OfflineGamesMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=18)
        self._offline_games_menu_container = self._create_offline_games_menu()

    def _create_offline_games_menu(self) -> Container:
        """Creates the container for the offline games menu"""
        return HSplit([
            VSplit([
                Box(self._container, padding=0, padding_right=1),
                ConditionalContainer(
                    Box(self.presenter.vs_computer_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == OfflineGamesMenuOptions.VS_COMPUTER)
                ),
            ])
        ])

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns the appropriate function bar fragments based on menu item selection"""
        fragments: StyleAndTextTuples = []
        if self.presenter.selection == OfflineGamesMenuOptions.VS_COMPUTER:
            fragments = self.presenter.vs_computer_menu_presenter.view.get_function_bar_fragments()
        return fragments

    def get_function_bar_key_bindings(self) -> ConditionalKeyBindings:
        """Returns the appropriate function bar key bindings based on menu item selection"""
        return ConditionalKeyBindings(
            self.presenter.vs_computer_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == OfflineGamesMenuOptions.VS_COMPUTER)
        )

    def __pt_container__(self) -> Container:
        return self._offline_games_menu_container
