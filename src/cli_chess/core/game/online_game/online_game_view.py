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
from cli_chess.core.game import PlayableGameViewBase
from cli_chess.utils.ui_common import handle_mouse_click
from prompt_toolkit.layout import Window, FormattedTextControl, VSplit, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game.online_game import OnlineGamePresenter


class OnlineGameView(PlayableGameViewBase):
    def __init__(self, presenter: OnlineGamePresenter):
        self.presenter = presenter
        super().__init__(presenter)

    def _accept_input(self, input: Buffer) -> None: # noqa
        """Accept handler for the input field"""
        self.presenter.user_input_received(input.text)
        self.input_field_container.text = ''

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments = self._base_function_bar_fragments()
            game_in_progress_fragments = ([
                ("class:function-bar.key", "F2", handle_mouse_click(self.presenter.propose_takeback)),
                ("class:function-bar.label", f"{'Takeback':<11}", handle_mouse_click(self.presenter.propose_takeback)),
                ("class:function-bar.spacer", " "),
                ("class:function-bar.key", "F3", handle_mouse_click(self.presenter.offer_draw)),
                ("class:function-bar.label", f"{'Offer draw':<11}", handle_mouse_click(self.presenter.offer_draw)),
                ("class:function-bar.spacer", " "),
                ("class:function-bar.key", "F4", handle_mouse_click(self.presenter.resign)),
                ("class:function-bar.label", f"{'Resign':<11}", handle_mouse_click(self.presenter.resign)),
                ("class:function-bar.spacer", " ")
            ])

            if self.presenter.is_game_in_progress():
                fragments.extend(game_in_progress_fragments)
            else:
                fragments.extend([
                    ("class:function-bar.key", "F10", handle_mouse_click(self.presenter.exit)),
                    ("class:function-bar.label", f"{'Exit':<11}", handle_mouse_click(self.presenter.exit))
                ])
            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
        ], height=D(max=1, preferred=1))

    def _container_key_bindings(self) -> KeyBindings:
        """Creates the key bindings for this container"""
        bindings = super()._container_key_bindings()

        @bindings.add(Keys.F2, filter=Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event): # noqa
            self.presenter.propose_takeback()

        @bindings.add(Keys.F3, filter=Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event):
            if not event.is_repeat:
                self.presenter.offer_draw()

        @bindings.add(Keys.F4, filter=Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event):
            if not event.is_repeat:
                self.presenter.resign()

        @bindings.add(Keys.F10, filter=~Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event): # noqa
            self.presenter.exit()

        return bindings
