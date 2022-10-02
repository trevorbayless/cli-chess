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
from prompt_toolkit.layout import Window, FormattedTextControl, Dimension, HSplit
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import get_app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus import SingleValueMenuOption, MultiValueMenuOption


class MenuView:
    def __init__(self, presenter, container_width: int):
        self.presenter = presenter
        self.container_width = container_width
        self.selected_option = 0
        self.key_bindings = self._create_key_bindings()
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the menu"""
        return HSplit([
            Window(
                FormattedTextControl(self._get_title_text_fragments),
                width=Dimension(max=self.container_width),
                height=Dimension(max=1),
            ),
            Window(
                FormattedTextControl(self._get_options_text_fragments, focusable=True, key_bindings=self.key_bindings),
                always_hide_cursor=True,
                width=Dimension(max=self.container_width),
                height=Dimension(max=len(self.presenter.get_menu_options())),
            )
        ])

    def _get_title_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu title"""
        return [
            ("class:menu.category_title", f"{self.presenter.get_menu_category().title:<{self.container_width}}"),
            ("class:menu", "\n")
        ]

    def _get_options_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu options"""
        tokens: StyleAndTextTuples = []

        def append_option(index: int, option: SingleValueMenuOption):
            selected = self.selected_option == index

            def option_clicked(mouse_event: MouseEvent):
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    return self.select_option(index)
                else:
                    return NotImplemented

            sel_class = ",unfocused-selected" if selected else ""
            if self.presenter.view.has_focus() and selected:
                sel_class = ",focused-selected"
                tokens.append(("[SetCursorPosition]", ""))

            tokens.append(("class:menu.option" + sel_class, f"{option.option_name:<{self.container_width}}", option_clicked))
            tokens.append(("class:menu", "\n"))

        for i, o in enumerate(self.presenter.get_menu_options()):
            append_option(i, o)

        tokens.pop()
        return tokens

    def _create_key_bindings(self):
        """Create the generic key bindings for menu navigation"""
        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        @bindings.add(Keys.ControlP)
        @bindings.add("k")
        def _(event):
            """Go to the previous menu option"""
            self.select_previous_option()

        @bindings.add(Keys.Down)
        @bindings.add(Keys.ControlN)
        @bindings.add("j")
        def _(event):
            self.select_next_option()

        return bindings

    def select_next_option(self) -> None:
        """Select the next option"""
        count = len(self.presenter.get_menu_options())
        self.selected_option = (self.selected_option + 1) % count
        self.presenter.select_handler(self.selected_option)

    def select_previous_option(self) -> None:
        """Select the previous option"""
        count = len(self.presenter.get_menu_options())
        self.selected_option = (self.selected_option - 1) % count
        self.presenter.select_handler(self.selected_option)

    def select_option(self, index: int) -> None:
        """Select the option at the passed in index"""
        self.focus()
        self.selected_option = index
        self.presenter.select_handler(self.selected_option)

    def has_focus(self):
        """Returns true if this container has focus"""
        return get_app().layout.has_focus(self._container)

    def focus(self):
        """Focus on this container"""
        get_app().layout.focus(self._container)

    def quit(self) -> None:
        """Quit the application"""
        get_app().exit()

    def __pt_container__(self) -> HSplit:
        return self._container


class MultiValueMenuView(MenuView):
    def __init__(self, presenter, container_width: int, column_width: int):
        super().__init__(presenter, container_width)
        self.column_width = column_width

    def _get_options_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu options"""
        tokens: StyleAndTextTuples = []

        def append_option(index: int, option: MultiValueMenuOption):
            selected = self.selected_option == index

            def label_click(mouse_event: MouseEvent):
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    return self.select_option(index)
                else:
                    return NotImplemented

            def value_click(mouse_event: MouseEvent):
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    return self.cycle_value(index)
                else:
                    return NotImplemented

            sel_class = ",unfocused-selected" if selected else ""
            if self.has_focus() and selected:
                sel_class = ",focused-selected"

            tokens.append(("class:menu.option" + sel_class, f"{option.option_title:<{self.column_width}}", label_click))
            tokens.append(("class:menu.multi-value" + sel_class, f"{option.values[option.selected_value['index']]:<{self.column_width}}", value_click))
            tokens.append(("class:menu", "\n"))

        for i, o in enumerate(self.presenter.get_menu_options()):
            append_option(i, o)

        tokens.pop()
        return tokens

    def _create_key_bindings(self) -> KeyBindings:
        bindings = super()._create_key_bindings()

        @bindings.add(Keys.Enter, eager=True)
        @bindings.add(" ", eager=True)
        def _(event):
            """Go to the next menu option"""
            self.presenter.get_menu_options()[self.selected_option].next_value()

        return bindings

    def cycle_value(self, index: int) -> None:
        """Cycle to the options next value"""
        super().select_option(index)
        self.presenter.get_menu_options()[self.selected_option].next_value()
