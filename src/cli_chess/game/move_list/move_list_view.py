from prompt_toolkit.layout.containers import Window, ConditionalContainer
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea
from prompt_toolkit import HTML


class MoveListView:
    def __init__(self, presenter, initial_output="No moves..."):
        self.presenter = presenter
        self.move_list_output = TextArea(text=initial_output,
                                         width=D(min=1, max=20),
                                         height=D(min=1, max=4),
                                         line_numbers=True,
                                         multiline=True,
                                         wrap_lines=False,
                                         focus_on_click=True,
                                         scrollbar=True,
                                         read_only=True)

        #self.container = Window(self.move_list_output, width = 20)
        self.container = ConditionalContainer(self.move_list_output, True)


    def update(self, output : str):
        """Updates the move list output with the passed in text"""
        self.move_list_output.text = output


    def __pt_container__(self) -> Window:
        """Returns the move_list container"""
        return self.container
