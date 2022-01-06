from cli_chess.menus import MainMenuPresenter
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from prompt_toolkit.output.color_depth import ColorDepth


async def run_app() -> None:
    app = Application(layout=Layout(MainMenuPresenter().view),
                      color_depth=ColorDepth.TRUE_COLOR,
                      mouse_support=True,
                      full_screen=True)

    result = await app.run_async()