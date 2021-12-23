from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea


class MaterialDifferenceView:
    def __init__(self, presenter):
        self.presenter = presenter
        self.difference_output = TextArea(text="",
                                          width=D(min=1, max=20),
                                          height=D(min=1, max=1),
                                          read_only=True,
                                          focusable=False,
                                          multiline=False,
                                          wrap_lines=False)
        self.container = ConditionalContainer(self.difference_output, True)


    def update(self, difference : str):
        """Updates the view output with the passed in text"""
        self.difference_output.text = difference


    def __pt_container__(self) -> ConditionalContainer:
        """Returns this views container"""
        return self.container