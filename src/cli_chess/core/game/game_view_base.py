from __future__ import annotations
from cli_chess.utils.ui_common import handle_mouse_click, go_back_to_main_menu, AlertContainer
from cli_chess.utils.logging import log
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout import Window, Container, FormattedTextControl, VSplit, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GamePresenterBase, PlayableGamePresenterBase


class GameViewBase(ABC):
    def __init__(self, presenter: GamePresenterBase) -> None:
        self.presenter = presenter
        self.board_output_container = presenter.board_presenter.view
        self.move_list_container = presenter.move_list_presenter.view
        self.material_diff_upper_container = presenter.material_diff_presenter.view_upper
        self.material_diff_lower_container = presenter.material_diff_presenter.view_lower
        self.player_info_upper_container = presenter.player_info_presenter.view_upper
        self.player_info_lower_container = presenter.player_info_presenter.view_lower
        self.clock_upper = presenter.clock_presenter.view_upper
        self.clock_lower = presenter.clock_presenter.view_lower
        self.alert = AlertContainer()
        self._container = self._create_container()

        log.debug(f"Created {type(self).__name__} (id={id(self)})")

    @abstractmethod
    def _create_container(self) -> Container:
        pass

    def _base_function_bar_fragments(self) -> StyleAndTextTuples:
        """Return the minimum function bar fragments for a game"""
        fragments = ([])
        fragments.extend(self._flip_board_fb_fragments())
        fragments.extend(self._exit_fb_fragments())
        return fragments

    def _flip_board_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for flipping the board"""
        return (
            ("class:function-bar.key", "F1", handle_mouse_click(self.presenter.flip_board)),
            ("class:function-bar.label", f"{'Flip board':<11}", handle_mouse_click(self.presenter.flip_board)),
            ("class:function-bar.spacer", " "),
        )

    def _exit_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for exiting the game view"""
        return (
            ("class:function-bar.key", "F8", handle_mouse_click(self.presenter.exit)),
            ("class:function-bar.label", f"{'Exit':<11}", handle_mouse_click(self.presenter.exit)),
            ("class:function-bar.spacer", " "),
        )

    def _create_function_bar(self) -> VSplit:
        """Creates the views function bar"""
        return VSplit([
            Window(FormattedTextControl(self._base_function_bar_fragments())),
        ], height=D(max=1, preferred=1))

    def get_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821:
        """Returns the key bindings for this container"""
        bindings = KeyBindings()

        @bindings.add(Keys.F1, eager=True)
        def _(event): # noqa
            self.presenter.flip_board()

        @bindings.add(Keys.F8, eager=True)
        def _(event): # noqa
            self.presenter.exit()

        return merge_key_bindings([bindings, self.move_list_container.key_bindings])

    @staticmethod
    def exit() -> None:
        """Exits this view and returns to the main menu"""
        go_back_to_main_menu()

    def __pt_container__(self) -> Container:
        """Return the view container"""
        return self._container


class PlayableGameViewBase(GameViewBase, ABC):
    """Implements a base game view which has a move input field"""
    def __init__(self, presenter: PlayableGamePresenterBase):
        self.presenter = presenter
        self.premove_container = presenter.premove_presenter.view
        self.input_field_container = self._create_input_field_container()
        super().__init__(presenter)

    @abstractmethod
    def _create_container(self) -> Container:
        pass

    def _takeback_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for propsing a takeback"""
        return (
            ("class:function-bar.key", "F2", handle_mouse_click(self.presenter.propose_takeback)),
            ("class:function-bar.label", f"{'Takeback':<11}", handle_mouse_click(self.presenter.propose_takeback)),
            ("class:function-bar.spacer", " "),
        )

    def _draw_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for offering a draw"""
        return (
            ("class:function-bar.key", "F3", handle_mouse_click(self.presenter.offer_draw)),
            ("class:function-bar.label", f"{'Offer draw':<11}", handle_mouse_click(self.presenter.offer_draw)),
            ("class:function-bar.spacer", " "),
        )

    def _resign_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for resigning"""
        return (
            ("class:function-bar.key", "F4", handle_mouse_click(self.presenter.resign)),
            ("class:function-bar.label", f"{'Resign':<11}", handle_mouse_click(self.presenter.resign)),
            ("class:function-bar.spacer", " "),
        )

    def _clear_premove_fb_fragments(self) -> Tuple:
        """Returns the function bar fragments for clearing the set premove"""
        return (
            ("class:function-bar.key", "Esc", handle_mouse_click(self.presenter.premove_presenter.clear_premove)),
            ("class:function-bar.label", f"{'Clear Premove':<11}", handle_mouse_click(self.presenter.premove_presenter.clear_premove)),
            ("class:function-bar.spacer", " "),
        )

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments = ([])
            fragments.extend(self._flip_board_fb_fragments())

            if self.presenter.is_game_in_progress():
                fragments.extend(self._takeback_fb_fragments())

                if not self.presenter.is_vs_ai():
                    fragments.extend(self._draw_fb_fragments())

                fragments.extend(self._resign_fb_fragments())
                if self.presenter.premove_presenter.is_premove_set():
                    fragments.extend(self._clear_premove_fb_fragments())
            else:
                fragments.extend(self._exit_fb_fragments())
            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
        ], height=D(max=1, preferred=1))

    def get_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821:
        """Returns the key bindings for this container"""
        bindings = KeyBindings()

        @bindings.add(Keys.F2, filter=Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event): # noqa
            self.presenter.propose_takeback()

        if not self.presenter.is_vs_ai():
            @bindings.add(Keys.F3, filter=Condition(self.presenter.is_game_in_progress), eager=True)
            def _(event):
                if not event.is_repeat:
                    self.presenter.offer_draw()

        @bindings.add(Keys.F4, filter=Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event):
            if not event.is_repeat:
                self.presenter.resign()

        @bindings.add(Keys.F8, filter=~Condition(self.presenter.is_game_in_progress), eager=True)
        def _(event): # noqa
            self.presenter.exit()

        @bindings.add(Keys.Escape, filter=Condition(self.presenter.premove_presenter.is_premove_set), eager=True)
        def _(event):
            self.presenter.premove_presenter.clear_premove()

        return merge_key_bindings([bindings, super().get_key_bindings()])

    def _create_input_field_container(self) -> TextArea:
        """Returns a TextArea to use as the input field"""
        input_field = TextArea(height=D(max=1),
                               prompt="Move:",
                               style="class:move-input",
                               multiline=False,
                               wrap_lines=True,
                               focus_on_click=True)

        input_field.accept_handler = self._accept_input
        return input_field

    def _accept_input(self, input: Buffer) -> None: # noqa
        """Accept handler for the input field"""
        self.presenter.user_input_received(input.text)
        self.input_field_container.text = ''
