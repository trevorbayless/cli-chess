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
from prompt_toolkit.layout import Window, FormattedTextControl, ConditionalContainer, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.application import get_app
from prompt_toolkit.widgets import Box
from cli_chess.utils.ui_common import handle_mouse_click
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from cli_chess.menus.main_menu import MainMenuOptions
from cli_chess.menus.play_offline_menu import PlayOfflineMenuOptions
from cli_chess.__metadata__ import __version__
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.root_menu import RootMenuPresenter


class RootMenuView:
    def __init__(self, presenter: RootMenuPresenter):
        self.presenter = presenter
        #self._function_bar_key_bindings = self._create_function_bar_key_bindings()
        self._root_key_bindings = self._create_key_bindings()
        self._function_bar = self._create_function_bar()
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the menu"""
        return HSplit([
            VSplit([
                Box(self.presenter.main_menu_presenter.view, padding=0, padding_right=1),
                ConditionalContainer(
                    Box(self.presenter.play_offline_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.main_menu_presenter.selection == MainMenuOptions.PLAY_OFFLINE)
                ),
                ConditionalContainer(
                    Box(self.presenter.vs_computer_menu_presenter.view, padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.main_menu_presenter.selection == MainMenuOptions.PLAY_OFFLINE)
                    & Condition(lambda: self.presenter.play_offline_menu_presenter.selection == PlayOfflineMenuOptions.VS_COMPUTER)
                ),
                ConditionalContainer(
                    Box(Window(FormattedTextControl("Play both sides settings container placeholder")), padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.main_menu_presenter.selection == MainMenuOptions.PLAY_OFFLINE)
                    & Condition(lambda: self.presenter.play_offline_menu_presenter.selection == PlayOfflineMenuOptions.PLAY_BOTH_SIDES)
                ),
                ConditionalContainer(
                    Box(Window(FormattedTextControl("Settings container placeholder")), padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.main_menu_presenter.selection == MainMenuOptions.SETTINGS)
                ),
                ConditionalContainer(
                    Box(Window(FormattedTextControl("About container placeholder")), padding=0, padding_right=1),
                    filter=~is_done
                    & Condition(lambda: self.presenter.main_menu_presenter.selection == MainMenuOptions.ABOUT)
                )
            ]),
            self._function_bar
        ], key_bindings=self._root_key_bindings)

    def _create_function_bar(self) -> HSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments: StyleAndTextTuples = []

            ###
            # Function bar fragments for PLAY OFFLINE
            ###
            if self.presenter.main_menu_presenter.selection == MainMenuOptions.PLAY_OFFLINE:
                @handle_mouse_click
                def handle_start_game() -> None:
                    self.presenter.vs_computer_menu_presenter.handle_start_game()

                fragments.extend([
                    ("class:function_bar.key", "F1", handle_start_game),
                    ("class:function_bar.label", f"{'Start game':<14}", handle_start_game),
                ])

            ##
            # Function bar fragments for SETTINGS
            ##
            if self.presenter.main_menu_presenter.selection == MainMenuOptions.SETTINGS:
                @handle_mouse_click
                def handle_apply_settings() -> None:
                    pass

                @handle_mouse_click
                def handle_reset_settings() -> None:
                    pass

                fragments.extend([
                    ("class:function_bar.key", "F1", handle_apply_settings),
                    ("class:function_bar.label", "Apply settings", handle_apply_settings),
                    ("class:function_bar.spacer", " "),
                    ("class:function_bar.key", "F9", handle_reset_settings),
                    ("class:function_bar.label", "Reset settings", handle_reset_settings),
                ])

            ##
            # Always included fragments
            ##
            @handle_mouse_click
            def handle_quit() -> None:
                get_app().exit()

            if fragments:
                fragments.append(("class:function_bar.spacer", " "))

            fragments.extend([
                ("class:function_bar.key", "F10", handle_quit),
                ("class:function_bar.label", f"{'Quit':<14}", handle_quit)
            ])

            return fragments

        return HSplit([
            VSplit([
                Window(FormattedTextControl(_get_function_bar_fragments)),
                Window(FormattedTextControl(f"cli-chess {__version__}"), align=WindowAlign.RIGHT)
            ], height=D(max=1), z_index=0)
        ],  align=VerticalAlign.BOTTOM)

    # def _create_function_bar_key_bindings(self) -> KeyBindings:
    #     """Creates the key bindings for the function bar"""
    #     ##
    #     # PLAY OFFLINE Key Bindings
    #     ##
    #     @Condition
    #     def _play_offline_selected():
    #         return
    #     po_kb = KeyBindings()
    #     ConditionalKeyBindings
    #
    #     ##
    #     # SETTINGS Key Bindings
    #     ##
    #     s_kb = KeyBindings()
    #
    #     ##
    #     # ABOUT Key Bindings
    #     ##
    #     a_kb = KeyBindings()

    def _create_key_bindings(self) -> KeyBindings:
        """Creates the key bindings for the menu manager"""
        bindings = KeyBindings()
        bindings.add(Keys.Right)(focus_next)
        bindings.add(Keys.ControlF)(focus_next)
        bindings.add(Keys.Tab)(focus_next)
        bindings.add("l")(focus_next)
        bindings.add(Keys.Left)(focus_previous)
        bindings.add(Keys.ControlB)(focus_previous)
        bindings.add(Keys.BackTab)(focus_previous)
        bindings.add("h")(focus_previous)

        # @bindings.add(Keys.F1)
        # def _(event):
        #     """Quit the application"""
        #     get_app().exit()
        #
        # #TESTING ONLY
        # @bindings.add(Keys.F10)
        # def _(event):
        #     # TODO: Properly implement this logic
        #     """Start the game (testing only)"""
        #     self.presenter.vs_computer_menu_presenter.handle_start_game()

        return bindings

    def __pt_container__(self):
        return self._container
