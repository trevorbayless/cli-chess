from __future__ import annotations
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, RadioList, Button, Box
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, VerticalAlign, HorizontalAlign
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

bindings = KeyBindings()
bindings.add("tab")(focus_next)
bindings.add("s-tab")(focus_previous)


class MainMenuView:
    def __init__(self, presenter: MainMenuPresenter):
        self.presenter = presenter
        self.menu_list = RadioList(self.presenter.get_menu_options())
        self.ok_button = Button(text="Ok", handler=self.presenter.ok_handler)
        self.quit_button = Button(text="Quit", handler=self.quit_handler)
        self.container = self.create_container()
        get_app().layout = Layout(self.container, self.menu_list)

    def create_container(self) -> Box:
        """Create the main dialog"""
        return Box(Frame(title=HTML("Welcome to cli-chess!"),
                         key_bindings=bindings,
                         body=HSplit(padding=1,
                                     children=[self.menu_list,
                                               HSplit([VSplit(align=HorizontalAlign.CENTER,
                                                              children=[self.ok_button,
                                                                        self.quit_button
                                                                        ])
                                                       ])
                                               ])
                         )
                   )

    def get_selected_option(self) -> str:
        """Returns the currently selected value"""
        return self.menu_list.current_value

    def quit_handler(self) -> None:
        """Handler for the 'Quit' button"""
        get_app().exit()

    def __pt_container__(self) -> Box:
        """Returns the main menu container"""
        return self.container
