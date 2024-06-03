from __future__ import annotations
from cli_chess.__metadata__ import __version__
from cli_chess.utils.ui_common import handle_mouse_click, exit_app, get_custom_style
from cli_chess.utils import is_windows_os, default, log
from cli_chess.utils.config import terminal_config
from prompt_toolkit.application import Application
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.layout import Layout, Window, Container, FormattedTextControl, VSplit, HSplit, VerticalAlign, WindowAlign, D
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.widgets import Box
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit import print_formatted_text, HTML
try:
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError  # noqa
except AssertionError:
    pass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainPresenter

main_view: Container


class MainView:
    def __init__(self, presenter: MainPresenter):
        try:
            self.presenter = presenter
            self.color_depth = terminal_config.get_value(terminal_config.Keys.TERMINAL_COLOR_DEPTH)
            self._container = self._create_main_container()

            self.app = Application(
                layout=Layout(self._container),
                color_depth=lambda: self.color_depth,
                mouse_support=True,
                full_screen=True,
                style=self._get_combined_styles(),
                refresh_interval=0.5
            )

            global main_view
            main_view = self

        except Exception as e:
            self._handle_startup_exceptions(e)

    def run(self) -> None:
        """Runs the main application"""
        with patch_stdout():
            self.app.run()

    def _create_main_container(self):
        """Creates the container for the main view"""
        return HSplit([
            VSplit([
                Box(self.presenter.main_menu_presenter.view, padding=0, padding_right=1),
            ]),
            HSplit([
                self._create_navigation_hint(),
                self._create_function_bar()
            ], align=VerticalAlign.BOTTOM)
        ], key_bindings=merge_key_bindings([self.get_global_key_bindings(), self._create_function_bar_key_bindings()]))

    @staticmethod
    def _create_navigation_hint() -> Box:
        """Creates the navigation hint container"""
        message = "Use [ARROWS] to navigate the menus. Use [SPACEBAR] or [ENTER] to modify values."
        return Box(
            Window(FormattedTextControl(HTML(f"<i>{message}</i>"), style="class:label.dim"), align=WindowAlign.CENTER),
            padding=0, padding_bottom=1, height=D(max=2)
        )

    def _create_function_bar(self) -> VSplit:
        """Create the conditional function bar"""
        def _get_function_bar_fragments() -> StyleAndTextTuples:
            fragments = self.presenter.main_menu_presenter.view.get_function_bar_fragments()

            if fragments:
                fragments.append(("class:function-bar.spacer", " "))

            fragments.extend([
                ("class:function-bar.key", "F8", handle_mouse_click(exit_app)),
                ("class:function-bar.label", f"{'Quit':<14}", handle_mouse_click(exit_app))
            ])

            return fragments

        return VSplit([
            Window(FormattedTextControl(_get_function_bar_fragments)),
            Window(FormattedTextControl(f"cli-chess {__version__}", style="class:label"), align=WindowAlign.RIGHT)
        ], height=D(max=1, preferred=1))

    def _create_function_bar_key_bindings(self) -> "_MergedKeyBindings":  # noqa: F821
        """Creates the key bindings for the function bar"""
        main_menu_fb_key_bindings = self.presenter.main_menu_presenter.view.get_function_bar_key_bindings()
        main_view_fb_key_bindings = KeyBindings()
        main_view_fb_key_bindings.add(Keys.F8)(exit_app)

        return merge_key_bindings([main_view_fb_key_bindings, main_menu_fb_key_bindings])

    def get_global_key_bindings(self) -> KeyBindings():
        """Returns the global key bindings to be used application wide"""
        bindings = KeyBindings()

        # Global binding to refresh style
        @bindings.add(Keys.ControlR, eager=True, is_global=True)
        def _(event): # noqa
            log.info("Requested application style refresh")
            self.app.style = self._get_combined_styles(hot_swap=True)
        return bindings

    def _get_combined_styles(self, hot_swap=False) -> "_MergedStyle":  # noqa: F821
        """Combines the cli-chess default style with a user
           supplied custom style and returns the result
        """
        try:
            return merge_styles([Style.from_dict(default), Style.from_dict(get_custom_style())])
        except Exception as e:
            log.critical(f"Error parsing custom style: {e}")
            if not hot_swap:
                self.print_error_to_terminal(title="Error parsing custom style", msg=str(e))
                exit(1)

            log.info("Ignoring invalid custom style and using default instead")
            return Style.from_dict(default)

    def print_error_to_terminal(self, msg: str, title="Error", ):
        """Prints an error to the terminal. This will only print
           statements when the application is not yet running in
           order to avoid tearing the output.
        """
        if (not hasattr(self, 'app') or not self.app.is_running) and msg:
            # NOTE: Print statements are separated in order to be able to print
            #  syntax errors which can have mismatched tags (e.g. with eval()).
            print_formatted_text(HTML(f"<red>{title}</red>"))
            print_formatted_text(msg)

    def _handle_startup_exceptions(self, e: Exception) -> None:
        """Handles exceptions caught during application startup"""
        log.critical(f"Error starting cli-chess: {str(e)}")
        if is_windows_os() and isinstance(e, NoConsoleScreenBufferError):
            print("Error starting cli-chess:\n"
                  "A Windows console was expected and not found.\n"
                  "Try running this program using cmd.exe instead.")
        else:
            self.print_error_to_terminal(title="Error starting cli-chess", msg=str(e))
        exit(1)

    def __pt_container__(self) -> Container:
        """Return the view container"""
        return self._container
