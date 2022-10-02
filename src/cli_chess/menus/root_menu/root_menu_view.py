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
from prompt_toolkit.layout import Layout, Window, FormattedTextControl, ConditionalContainer, VSplit
from prompt_toolkit.filters import Condition, is_done
from prompt_toolkit.widgets import Box
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from cli_chess.menus.main_menu import MainMenuOptions
from cli_chess.menus.play_offline_menu import PlayOfflineMenuOptions
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.root_menu import RootMenuPresenter


class RootMenuView:
    def __init__(self, presenter: RootMenuPresenter):
        self.presenter = presenter
        self._container = self._create_container()
        self.key_bindings = self._create_key_bindings()

    def _create_container(self):
        """Creates the container for the menu"""
        return VSplit([
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
        ])

    def _create_key_bindings(self):
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
        return bindings

    def __pt_container__(self):
        return self._container
