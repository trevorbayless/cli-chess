from cli_chess.ui import MainMenu
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from prompt_toolkit.output.color_depth import ColorDepth

def start_app() -> None:
    app = Application(layout=Layout(MainMenu()),
                      color_depth=ColorDepth.TRUE_COLOR,
                      mouse_support=True,
                      full_screen=True)
    app.run()
