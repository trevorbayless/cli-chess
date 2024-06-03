from __future__ import annotations
from cli_chess.utils import AlertType, log
from cli_chess.utils.common import VALID_COLOR_DEPTHS
from cli_chess.utils.config import get_config_path
from prompt_toolkit.layout import Window, FormattedTextControl, ConditionalContainer
from prompt_toolkit.filters import to_filter
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.key_binding import KeyPressEvent, merge_key_bindings
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout, Container
from typing import TypeVar, Callable, cast
import os

E = TypeVar("E", bound=Callable[[KeyPressEvent], None])
T = TypeVar("T", bound=Callable[[MouseEvent], None])


def go_back_to_main_menu() -> None:
    """Returns to the main menu"""
    from cli_chess.core.main.main_view import main_view
    change_views(main_view)


def change_views(container: Container, focused_element=None):
    """Change the view to the passed in container.
       Focuses the view on the optional passed in element.
    """
    log.debug(f"View changed to {type(container).__name__} (id={id(container)})")
    app = get_app()
    focused_element = focused_element if focused_element else container
    app.layout = Layout(container)

    try:
        app.key_bindings = None
        app.layout.focus(focused_element)

        # NOTE: There's a possible PT bug here. There shouldn't be a need to
        #  assign the current container bindings to the application. The bindings
        #  should be picked up automatically (and are the majority of the time).
        #  However, I've seen this drop bindings multiple times (e.g. if spamming
        #  a menu change quickly, or sometimes after clicking the function bar).
        from cli_chess.core.main.main_view import main_view
        app.key_bindings = merge_key_bindings([container.get_key_bindings(), main_view.get_global_key_bindings()])  # noqa
    except (ValueError, AttributeError):
        # ValueError is expected on elements that cannot be focused. Proceed regardless.
        # AttributeError is expected on containers that don't define `get_key_bindings()`.
        # In the case of AttributeError, PT will look at each container to grab bindings.
        pass

    repaint_ui()


def repaint_ui() -> None:
    """Force the ui to repaint"""
    get_app().invalidate()


def exit_app(*args) -> None: # noqa
    """Exit the application"""
    get_app().exit()


def handle_bound_key_pressed(handler: E) -> E:
    """Decorator/handler for key events to avoid having to pass the key event around"""
    def bound_key_pressed(key_event: KeyPressEvent): # noqa
        return handler()

    return cast(E, bound_key_pressed)


def handle_mouse_click(handler: T) -> T:
    """Decorator to handle mouse click events"""
    def mouse_down(mouse_event: MouseEvent):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            return handler()
        else:
            return NotImplemented

    return cast(T, mouse_down)


def set_color_depth(depth: str) -> None:
    """Sets the color depth to the depth passed in"""
    if depth in VALID_COLOR_DEPTHS:
        from cli_chess.core.main.main_view import main_view
        log.info(f"Setting color depth to: {depth}")
        main_view.color_depth = depth
        repaint_ui()


def get_custom_style() -> dict:
    """Returns the user defined custom style"""
    try:
        custom_style_path = get_config_path() + "custom_style.py"
        if not os.path.isfile(custom_style_path) or os.stat(custom_style_path).st_size == 0:
            create_skeleton_custom_style()

        with open(custom_style_path, 'r') as file:
            custom_style = file.read()
            return eval(custom_style)
    except Exception as e:
        log.critical(f"Custom style error: {e}")
        raise


def create_skeleton_custom_style() -> None:
    """Creates (or overwrites) the 'custom_style.py' file.
       Raises an exception on generation errors.
    """
    try:
        custom_style_path = get_config_path() + "custom_style.py"
        with open(custom_style_path, 'w') as file:
            file.write("# This file is used to override the default style of cli-chess. It must be kept in dictionary format.\n")
            file.write("# Colors are expected to be HTML color names (e.g. seagreen) or HTML hex colors (e.g. #2E8B57)\n")
            file.write("# Restarting cli-chess or pressing [CTRL+R] on any screen will force a style refresh.\n")
            file.write("# Visit the cli-chess github page (https://github.com/trevorbayless/cli-chess/) for more styling information.\n\n")
            file.write("{\n\n")
            file.write("}")
    except Exception:
        raise


class AlertContainer:
    """A container that can be added to views to handle displaying alerts"""
    def __init__(self):
        self._alert_label = FormattedTextControl(text="", show_cursor=False)
        self._alert_container = self._create_alert_container()

    def _create_alert_container(self) -> ConditionalContainer:
        """Create the error container"""
        return ConditionalContainer(
            Window(self._alert_label, always_hide_cursor=True, wrap_lines=True),
            filter=to_filter(False)
        )

    def show_alert(self, text: str, alert_type=AlertType.ERROR) -> None:
        """Displays the alert label with the text passed in"""
        self._alert_label.text = text
        self._alert_label.style = alert_type.get_style(alert_type)
        self._alert_container.filter = to_filter(True)
        repaint_ui()

    def clear_alert(self) -> None:
        """Clears the alert container"""
        self._alert_label.text = ""
        self._alert_container.filter = to_filter(False)
        repaint_ui()

    def __pt_container__(self):
        return self._alert_container
