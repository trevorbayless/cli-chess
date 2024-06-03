from __future__ import annotations
from cli_chess.menus import MenuView
from cli_chess.utils.ui_common import handle_mouse_click, handle_bound_key_pressed
from prompt_toolkit.layout import Container, VSplit, HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.tv_channel_menu import TVChannelMenuPresenter


class TVChannelMenuView(MenuView):
    def __init__(self, presenter: TVChannelMenuPresenter):
        self.presenter = presenter
        super().__init__(self.presenter, container_width=20)
        self._tv_channels_menu_container = self._create_tv_channels_menu()

    def _create_tv_channels_menu(self) -> Container:
        """Creates the container for the tv channels menu"""
        return HSplit([
            VSplit([
                Box(self._container, padding=0, padding_right=1),
            ]),
        ])

    def get_function_bar_fragments(self) -> StyleAndTextTuples:
        """Returns the tv menu function bar fragments"""
        return [
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.handle_start_watching_tv)),
            ("class:function-bar.label", f"{'Watch channel':<14}", handle_mouse_click(self.presenter.handle_start_watching_tv)),
        ]

    def get_function_bar_key_bindings(self) -> KeyBindings:
        """Returns the function bar key bindings to use for the tv menu"""
        bindings = KeyBindings()
        bindings.add(Keys.F1)(handle_bound_key_pressed(self.presenter.handle_start_watching_tv))
        return bindings

    def __pt_container__(self) -> Container:
        return self._tv_channels_menu_container
