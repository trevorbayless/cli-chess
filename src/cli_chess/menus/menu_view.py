from __future__ import annotations
from cli_chess.utils.ui_common import handle_mouse_click
from prompt_toolkit.layout import Window, FormattedTextControl, HSplit, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import get_app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuPresenter, MultiValueMenuPresenter


class MenuView:
    def __init__(self, presenter: MenuPresenter, container_width: int):
        self.presenter = presenter
        self.container_width = container_width
        self.selected_option = 0
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the menu"""
        return HSplit([
            Window(
                FormattedTextControl(self._get_title_text_fragments),
                height=D(max=1),
            ),
            Window(
                FormattedTextControl(self._get_options_text_fragments, focusable=True),
                always_hide_cursor=True,
                height=D(max=len(self.presenter.get_menu_options())),
            )
        ], width=D(max=self.container_width), key_bindings=self._create_key_bindings())

    def _get_title_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu title"""
        return [
            ("class:menu.category-title", f"{self.presenter.get_menu_category().title:<{self.container_width}}"),
            ("class:menu", "\n")
        ]

    def _get_options_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu options"""
        tokens: StyleAndTextTuples = []

        def append_option(index: int, option: MenuOption):
            selected = self.selected_option == index

            @handle_mouse_click
            def option_clicked():
                self.select_option(index)

            sel_class = ",unfocused-selected" if selected else ""
            if self.presenter.view.has_focus() and selected:
                sel_class = ",focused-selected"
                tokens.append(("[SetCursorPosition]", ""))

            tokens.append(("class:menu.option" + sel_class, f"{option.option_name:<{self.container_width}}", option_clicked))
            tokens.append(("class:menu", "\n"))

        for i, opt in enumerate(self.presenter.get_visible_menu_options()):
            append_option(i, opt)

        tokens.pop()
        return tokens

    def _create_key_bindings(self) -> KeyBindings:
        """Create the generic key bindings for menu navigation"""
        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        @bindings.add(Keys.ControlP)
        def _(event): # noqa
            """Go to the previous menu option"""
            self.select_previous_option()

        @bindings.add(Keys.Down)
        @bindings.add(Keys.ControlN)
        def _(event): # noqa
            self.select_next_option()

        return bindings

    def select_next_option(self) -> None:
        """Select the next option"""
        count = len(self.presenter.get_visible_menu_options())
        self.selected_option = (self.selected_option + 1) % count
        self.presenter.select_handler(self.selected_option)

    def select_previous_option(self) -> None:
        """Select the previous option"""
        count = len(self.presenter.get_visible_menu_options())
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

    def __pt_container__(self) -> HSplit:
        return self._container


class MultiValueMenuView(MenuView):
    def __init__(self, presenter: MultiValueMenuPresenter, container_width: int, column_width: int):
        self.presenter = presenter
        self.column_width = column_width
        super().__init__(self.presenter, container_width)

    def _get_options_text_fragments(self) -> StyleAndTextTuples:
        """Create the text fragments for the menu options"""
        tokens: StyleAndTextTuples = []

        def append_option(index: int, menu_option: MultiValueMenuOption):
            selected = self.selected_option == index

            @handle_mouse_click
            def label_click():
                self.select_option(index)

            @handle_mouse_click
            def value_click():
                self.select_option(index)
                self.cycle_value(index)

            sel_class = ",unfocused-selected" if selected else ""
            if self.has_focus() and selected:
                sel_class = ",focused-selected"

            tokens.append(("class:menu.option" + sel_class, f"{menu_option.option_name:<{self.column_width}}", label_click))
            tokens.append(("class:menu.multi-value" + sel_class, f"{menu_option.values[menu_option.selected_value['index']]:<{self.column_width}}", value_click))  # noqa: E501
            tokens.append(("class:menu", "\n"))

        for i, opt in enumerate(self.presenter.get_visible_menu_options()):
            append_option(i, opt)

        tokens.pop()
        return tokens

    def _create_key_bindings(self) -> KeyBindings:
        bindings = super()._create_key_bindings()

        @bindings.add(Keys.Enter, eager=True)
        @bindings.add(" ", eager=True)
        def _(event): # noqa
            """Handle Enter/Space key press"""
            self.cycle_value(self.selected_option)

        return bindings

    def cycle_value(self, index: int) -> None:
        """Cycle to the next value of the selected option"""
        self.presenter.get_visible_menu_options()[index].next_value()
        super().select_option(index)
        self.presenter.value_cycled_handler(self.selected_option)
