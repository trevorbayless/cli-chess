from prompt_toolkit import HTML, print_formatted_text as print
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.layout.containers import Container, ConditionalContainer, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.layout import Layout

class GameView:
    def __init__(self, presenter):
        self.presenter = presenter
        self.board_output_display = FormattedTextControl("No board set", )
        self.move_list_display = self.create_move_list()
        self.input_field = self.create_input_field()
        self.container = self.create_container()
        get_app().layout = Layout(self.container, self.input_field)


    def create_container(self) -> Container:
        return HSplit(
            [
                VSplit(
                    [
                        Window(self.board_output_display, width=20),
                        HSplit([self.move_list_display])
                    ]),
                self.input_field
            ]
        )


    def create_move_list(self) -> TextArea:
        """Returns a TextArea to hold the move list"""
        return ConditionalContainer(TextArea(text="No moves...",
                                             width=D(min=1, max=20),
                                             height=D(min=1, max=4),
                                             line_numbers=True,
                                             multiline=True,
                                             wrap_lines=False,
                                             focus_on_click=True,
                                             scrollbar=True,
                                             read_only=False), True)


    def create_input_field(self) -> TextArea:
        """Returns a TextArea to use as the input field"""
        input_type = "GAME"
        input_field =  TextArea(height=1,
                                prompt=HTML(f"<style bg='darkcyan'>[{input_type}] $ </style>"),
                                style="class:input-field",
                                multiline=False,
                                wrap_lines=True,
                                focus_on_click=True)

        input_field.accept_handler = self.accept_input
        return input_field


    def accept_input(self, input):
        """Called enter is pressed on the input field"""
        if input.text == "quit":
            get_app().exit()
        else:
            self.presenter.input_received(input.text)
            self.input_field.text = ''


    def update_board_output(self, board_output : str):
        self.board_output_display.text = HTML(board_output)


    def __pt_container__(self) -> Container:
        """Returns the game_view container"""
        return self.container
