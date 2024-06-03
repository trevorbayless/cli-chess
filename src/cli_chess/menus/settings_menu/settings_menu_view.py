from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.menus.settings_menu import SettingsMenuOptions
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, HSplit
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.key_binding import ConditionalKeyBindings
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.settings_menu import SettingsMenuPresenter


class SettingsMenuView(MenuView):
    def __init__(self, presenter: SettingsMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=27)
        self._settings_menu_container = self._create_settings_menu()

    def _create_settings_menu(self) -> Container:
        """Creates the container for the settings menu"""
        return HSplit([
            VSplit([
                Box(self._container, padding=0, padding_right=1),
                ConditionalContainer(
                    Box(self.presenter.token_manger_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == SettingsMenuOptions.LICHESS_AUTHENTICATION)
                ),
                ConditionalContainer(
                    Box(self.presenter.program_settings_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == SettingsMenuOptions.PROGRAM_SETTINGS)
                ),
            ]),
        ])

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns the appropriate function bar fragments based on menu item selection"""
        fragments: StyleAndTextTuples = []
        if self.presenter.selection == SettingsMenuOptions.LICHESS_AUTHENTICATION:
            fragments = self.presenter.token_manger_presenter.view.get_function_bar_fragments()
        return fragments

    def get_function_bar_key_bindings(self) -> ConditionalKeyBindings:  # noqa: F821
        """Returns the appropriate function bar key bindings based on menu item selection"""
        return ConditionalKeyBindings(
            self.presenter.token_manger_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == SettingsMenuOptions.LICHESS_AUTHENTICATION)
        )

    def __pt_container__(self) -> Container:
        return self._settings_menu_container
