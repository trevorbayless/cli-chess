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

from cli_chess.utils.logging import log
from cli_chess.menus.main_menu import MainMenuModel, MainMenuOptions
from cli_chess.menus import MenuView, MenuPresenter


class MainMenuPresenter(MenuPresenter):
    """Defines the Main Menu"""
    def __init__(self, model: MainMenuModel):
        self.model = model
        self.view = MenuView(self, container_width=15)  # Todo: Get and set to longest option length?
        self.selection = self.model.get_menu_options()[0].option
        super().__init__(self.model, self.view)

    def select_handler(self, selected_option: int):
        """Handles option selection"""
        try:
            self.selection = self.model.get_menu_options()[selected_option].option
            log.info(f"menu_selection: {self.selection}")

            if self.selection == MainMenuOptions.PLAY_OFFLINE:
                pass
            elif self.selection == MainMenuOptions.SETTINGS:
                pass
            elif self.selection == MainMenuOptions.ABOUT:
                pass
            elif self.selection == MainMenuOptions.QUIT:
                log.info("User quit")
                self.view.quit()
            else:
                # Todo: Print error to view element
                raise ValueError(f"Invalid menu option: {self.selection}")
        except Exception as e:
            # Todo: Print error to view element
            log.exception(f"Exception caught: {e}")
            raise e

