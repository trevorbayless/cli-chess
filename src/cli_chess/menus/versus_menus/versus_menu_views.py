from __future__ import annotations
from cli_chess.menus import MultiValueMenuView
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.versus_menus.versus_menu_presenters import VersusMenuPresenter


class VersusMenuView(MultiValueMenuView):
    def __init__(self, presenter: VersusMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=38, column_width=18)

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.handle_start_game)),
            ("class:function-bar.label", f"{'Start game':<14}", handle_mouse_click(self.presenter.handle_start_game)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Creates the key bindings associated to the function bar fragments"""
        kb = KeyBindings()
        kb.add(Keys.F1)(handle_bound_key_pressed(self.presenter.handle_start_game))
        return kb
