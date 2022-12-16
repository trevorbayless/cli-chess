# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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
from cli_chess.menus import MenuView
from cli_chess.menus.main_menu import MainMenuOptions
from prompt_toolkit.layout import Container, Window, FormattedTextControl, ConditionalContainer, VSplit, HSplit
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.widgets import Box
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
                    Box(self.presenter.online_games_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.ONLINE_GAMES)
                ),
                ConditionalContainer(
                    Box(self.presenter.offline_games_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.OFFLINE_GAMES)
                ),
                ConditionalContainer(
                    Box(self.presenter.settings_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.SETTINGS)
                ),
                ConditionalContainer(
                    Box(Window(FormattedTextControl("About container placeholder")), padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.selection == MainMenuOptions.ABOUT)
                )
            ]),
        ], key_bindings=self._container_key_bindings())

    @staticmethod
    def _container_key_bindings() -> KeyBindings:
        """Creates the key bindings for this container"""
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
        if self.presenter.selection == MainMenuOptions.OFFLINE_GAMES:
            fragments = self.presenter.offline_games_menu_presenter.view.get_function_bar_fragments()
        return fragments

    def get_function_bar_key_bindings(self) -> ConditionalKeyBindings:
        """Returns the appropriate function bar key bindings based on menu item selection"""
        kb = ConditionalKeyBindings(
            self.presenter.offline_games_menu_presenter.view.get_function_bar_key_bindings(),
            filter=Condition(lambda: self.presenter.selection == MainMenuOptions.OFFLINE_GAMES)
        )
        return kb

    def __pt_container__(self) -> Container:
        return self.main_menu_container
