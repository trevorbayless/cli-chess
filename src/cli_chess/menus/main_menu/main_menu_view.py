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
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, RadioList, Button, Box
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, HorizontalAlign
from prompt_toolkit.layout.dimension import D
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
        self.container = self.create_container()
        get_app().layout = Layout(self.container, self.menu_list)

    def create_container(self) -> Box:
        """Creates the main menu container"""
        boxed_options = Box(body=self.menu_list,
                            width=D(max=30, preferred=30),
                            padding_top=D(max=1),
                            padding_bottom=D(max=1),
                            padding_left=D(max=4),
                            padding_right=D(max=4))

        ok_button = Button(text="Ok", handler=self.presenter.ok_handler)
        quit_button = Button(text="Quit", handler=self.quit_handler)

        menu_contents = Frame(title=HTML("Welcome to cli-chess!"),
                              key_bindings=bindings,
                              body=HSplit([boxed_options,
                                          VSplit([ok_button, quit_button],
                                                 align=HorizontalAlign.CENTER)
                                           ])
                              )

        return Box(menu_contents)

    def get_selected_option(self) -> str:
        """Returns the currently selected value"""
        return self.menu_list.current_value

    def quit_handler(self) -> None:
        """Handler for the 'Quit' button"""
        get_app().exit()

    def __pt_container__(self) -> Box:
        """Returns the main menu container"""
        return self.container
