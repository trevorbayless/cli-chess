from __future__ import annotations
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, Label, RadioList, Button, Box
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.application import get_app


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
                         body=HSplit(
                                [
                                    Label(text="What would you like to do?"),
                                    self.menu_list,
                                    VSplit(
                                        [
                                            self.ok_button,
                                            self.quit_button
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
