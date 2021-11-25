from prompt_toolkit.widgets import TextArea, Label, Button, Dialog
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.application import get_app

def show_about() -> None:
    """Sets the app layout to the Main Menu"""
    about = About()
    get_app().layout = Layout(about, about.ok_button)


class About:
    """Class to create the About screen"""
    def __init__(self):
        self.ok_button = Button(text="Ok", handler=self.ok_handler)
        self.dialog = self.create_dialog()
        self.previous_screen = get_app().layout


    def create_dialog(self) -> Dialog:
        """Create the Dialog wrapper"""
        return Dialog(title="cli-chess",
                      body=HSplit(
                          [
                              Label(text="About.", dont_extend_height=True)
                          ],
                          padding=D(preferred=1, max=1),
                      ),
                      buttons=[self.ok_button],
                      with_background=True)


    def ok_handler(self) -> str:
        """Handler for the 'Ok' button.
           Returns to the previous container
        """
        get_app().layout = self.previous_screen


    def __pt_container__(self) -> Dialog:
        """Returns the dialog for container use"""
        return self.dialog