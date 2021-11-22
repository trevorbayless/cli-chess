from .board import BoardView
from prompt_toolkit import HTML, print_formatted_text as print
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.layout.containers import Container, ConditionalContainer, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.layout import Layout

class GameViewBase:
    def __init__(self, presenter, board_view):
        self.presenter = presenter
        self.board_output_container = board_view.get_container()
        self.move_list_container = self._create_move_list_container()
        self.input_field_container = self._create_input_field_container()


    def _create_move_list_container(self) -> TextArea:
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


    def _create_input_field_container(self) -> TextArea:
        """Returns a TextArea to use as the input field"""
        input_type = "GAME"
        input_field =  TextArea(height=1,
                                prompt=HTML(f"<style bg='darkcyan'>[{input_type}] $ </style>"),
                                style="class:input-field",
                                multiline=False,
                                wrap_lines=True,
                                focus_on_click=True)

        input_field.accept_handler = self._accept_input
        return input_field


    def _accept_input(self, input):
        """The accept handler for the input field"""
        if input.text == "quit":
            get_app().exit()
        else:
            self.presenter.input_received(input.text)
            self.input_field_container.text = ''


    def get_board_output_container(self) -> FormattedTextControl:
        return self.board_output_container


    def get_move_list_container(self) -> TextArea:
        """Returns the move list container"""
        return self.move_list_container


    def get_input_field_container(self) -> TextArea:
        """Returns the input field container"""
        return self.input_field_container


class GameView(GameViewBase):
    def __init__(self, presenter, board_view : BoardView):
        super().__init__(presenter, board_view)
        self.container = self.create_container()
        get_app().layout = Layout(self.container, super().get_input_field_container())


    def create_container(self) -> Container:
        return HSplit(
            [
                VSplit(
                    [
                        super().get_board_output_container(),
                        HSplit([super().get_move_list_container()])
                    ]),
                super().get_input_field_container()
            ]
        )


    def __pt_container__(self) -> Container:
        """Returns the game_view container"""
        return self.container
