from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.menus.online_games_menu import OnlineGamesMenuOptions
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, HSplit
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.key_binding import merge_key_bindings, ConditionalKeyBindings
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.online_games_menu import OnlineGamesMenuPresenter


class OnlineGamesMenuView(MenuView):
    def __init__(self, presenter: OnlineGamesMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=20)
        self._online_games_menu_container = self._create_online_games_menu()

    def _create_online_games_menu(self) -> Container:
        """Creates the container for the online games menu"""
        return HSplit([
            VSplit([
                Box(self._container, padding=0, padding_right=1),
                ConditionalContainer(
                    Box(self.presenter.vs_random_opponent_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.CREATE_GAME)
                ),
                ConditionalContainer(
                    Box(self.presenter.vs_computer_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.VS_COMPUTER_ONLINE)
                ),
                ConditionalContainer(
                    Box(self.presenter.tv_channel_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.WATCH_LICHESS_TV)
                ),
            ]),
        ])

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns the appropriate function bar fragments based on menu item selection"""
        fragments: StyleAndTextTuples = []
        if self.presenter.selection == OnlineGamesMenuOptions.CREATE_GAME:
            fragments = self.presenter.vs_random_opponent_menu_presenter.view.get_function_bar_fragments()
        if self.presenter.selection == OnlineGamesMenuOptions.VS_COMPUTER_ONLINE:
            fragments = self.presenter.vs_computer_menu_presenter.view.get_function_bar_fragments()
        if self.presenter.selection == OnlineGamesMenuOptions.WATCH_LICHESS_TV:
            fragments = self.presenter.tv_channel_menu_presenter.view.get_function_bar_fragments()
        return fragments

    def get_function_bar_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821
        """Returns the appropriate function bar key bindings based on menu item selection"""
        vs_random_opponent_kb = ConditionalKeyBindings(
            self.presenter.vs_random_opponent_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.CREATE_GAME)
        )

        vs_ai_kb = ConditionalKeyBindings(
            self.presenter.vs_computer_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.VS_COMPUTER_ONLINE)
        )

        tv_kb = ConditionalKeyBindings(
            self.presenter.tv_channel_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == OnlineGamesMenuOptions.WATCH_LICHESS_TV)
        )

        return merge_key_bindings([vs_random_opponent_kb, vs_ai_kb, tv_kb])

    def __pt_container__(self) -> Container:
        return self._online_games_menu_container
