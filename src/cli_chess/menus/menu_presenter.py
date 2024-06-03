from __future__ import annotations
from cli_chess.utils.logging import log
from cli_chess.utils.event import Event
from enum import Enum
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.menus import MenuOption, MultiValueMenuOption, MenuCategory, MenuModel, MultiValueMenuModel, MenuView, MultiValueMenuView


class MenuPresenter:
    def __init__(self, model: MenuModel, view: MenuView):
        self.model = model
        self.view = view
        self.selection = self.model.get_menu_options()[0].option
        self.e_selection_updated = Event()

    def get_menu_category(self) -> MenuCategory:
        """Get the menu category"""
        return self.model.get_menu_category()

    def get_menu_options(self) -> List[MenuOption]:
        """Returns all menu options regardless of their enabled/visibility state"""
        return self.model.get_menu_options()

    def get_visible_menu_options(self) -> List[MenuOption]:
        """Returns all menu options which are visible"""
        visible_options = []
        for opt in self.get_menu_options():
            if not opt.visible:
                continue
            else:
                visible_options.append(opt)
        return visible_options

    def select_handler(self, selected_option: int):
        """Called on menu item selection. Classes that inherit from
           this class should override this method if specific tasks
           need to execute when the selected option changes
        """
        try:
            self.selection = self.model.get_menu_options()[selected_option].option
            log.debug(f"Menu selection: {self.selection}")
            self._notify_selection_updated(self.selection)

        except Exception as e:
            # Todo: Print error to view element
            log.exception(f"Exception caught: {e}")
            raise e

    def has_focus(self) -> bool:
        """Queries the view to determine if the menu has focus"""
        return self.view.has_focus()

    def _notify_selection_updated(self, selected_option: int) -> None:
        """Notifies listeners that the selection has been updated"""
        self.e_selection_updated.notify(selected_option)


class MultiValueMenuPresenter(MenuPresenter):
    def __init__(self, model: MultiValueMenuModel, view: MultiValueMenuView):
        self.model = model
        self.view = view
        super().__init__(self.model, self.view)

    def value_cycled_handler(self, selected_option: Enum) -> None:
        """Called when the selected options value is cycled. Classes that inherit from
           this class should override this method if they need to
           be alerted when the selected option changes
        """
        pass

    def get_menu_options(self) -> List[MultiValueMenuOption]:
        """Returns all menu options regardless of their enabled/visibility state"""
        return super().get_menu_options()

    def get_visible_menu_options(self) -> List[MultiValueMenuOption]:
        """Returns all menu options which are visible"""
        return super().get_visible_menu_options()
