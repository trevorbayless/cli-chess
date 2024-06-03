from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.menus.main_menu import MainMenuOptions
from cli_chess.core.api.api_manager import api_is_ready
from cli_chess.__metadata__ import __url__
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, HSplit
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.widgets import Box, TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.main_menu import MainMenuPresenter


class MainMenuView(MenuView):
    def __init__(self, presenter: MainMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=15)
        self.main_menu_container = self._create_main_menu()

    def _create_main_menu(self) -> Container:
        """Creates the container for the main menu"""
        return HSplit([
            VSplit([
                Box(self._container, padding=0, padding_right=1),
                ConditionalContainer(
                    Box(self.presenter.offline_games_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.OFFLINE_GAMES)
                ),
                ConditionalContainer(
                    TextArea(
                        "Missing API Token or API client unavailable.\n"
                        "Go to 'Settings' to link your Lichess API token.\n\n"
                        "For further assistance check out the Github page:\n"
                        f"{__url__}",
                        wrap_lines=True, read_only=True, focusable=False
                    ),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.ONLINE_GAMES)
                    & ~Condition(api_is_ready)
                ),
                ConditionalContainer(
                    Box(self.presenter.online_games_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.ONLINE_GAMES)
                    & Condition(api_is_ready)
                ),
                ConditionalContainer(
                    Box(self.presenter.settings_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.SETTINGS)
                ),
                ConditionalContainer(
                    Box(self.presenter.about_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.ABOUT)
                )
            ]),
        ], key_bindings=self.get_key_bindings())

    @staticmethod
    def get_key_bindings() -> KeyBindings:
        """Returns the key bindings for this container"""
        bindings = KeyBindings()
        bindings.add(Keys.Right)(focus_next)
        bindings.add(Keys.ControlF)(focus_next)
        bindings.add(Keys.Tab)(focus_next)
        bindings.add(Keys.Left)(focus_previous)
        bindings.add(Keys.ControlB)(focus_previous)
        bindings.add(Keys.BackTab)(focus_previous)
        return bindings

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns the appropriate function bar fragments based on menu item selection"""
        fragments: StyleAndTextTuples = []
        if self.presenter.selection == MainMenuOptions.ONLINE_GAMES:
            fragments = self.presenter.online_games_menu_presenter.view.get_function_bar_fragments()
        elif self.presenter.selection == MainMenuOptions.OFFLINE_GAMES:
            fragments = self.presenter.offline_games_menu_presenter.view.get_function_bar_fragments()
        elif self.presenter.selection == MainMenuOptions.SETTINGS:
            fragments = self.presenter.settings_menu_presenter.view.get_function_bar_fragments()
        elif self.presenter.selection == MainMenuOptions.ABOUT:
            fragments = self.presenter.about_presenter.view.get_function_bar_fragments()
        return fragments

    def get_function_bar_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821
        """Returns the appropriate function bar key bindings based on menu item selection"""
        online_games_kb = ConditionalKeyBindings(
            self.presenter.online_games_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == MainMenuOptions.ONLINE_GAMES)
        )

        offline_games_kb = ConditionalKeyBindings(
            self.presenter.offline_games_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == MainMenuOptions.OFFLINE_GAMES)
        )

        settings_kb = ConditionalKeyBindings(
            self.presenter.settings_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == MainMenuOptions.SETTINGS)
        )

        about_kb = ConditionalKeyBindings(
            self.presenter.about_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == MainMenuOptions.ABOUT)
        )
        return merge_key_bindings([online_games_kb, offline_games_kb, settings_kb, about_kb])

    def __pt_container__(self) -> Container:
        return self.main_menu_container
