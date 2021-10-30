from .game_presenter import GamePresenter
from prompt_toolkit import HTML, print_formatted_text as print
from prompt_toolkit.widgets import Frame, TextArea, Box
from prompt_toolkit.layout.containers import Container, HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

class GameView:
    def __init__(self):
        self.presenter = GamePresenter()
        self.window = self.create_container()

    
    def create_container(self) -> Container:
        return HSplit([VSplit([self.board_window(), self.chat_window()]), self.input_area()])


    def board_window(self) -> Window:
        return Window(FormattedTextControl(HTML(self.presenter.get_board_output())), width=20)


    def chat_window(self) -> Window:
        return Frame(Window(FormattedTextControl(HTML(f"<b>player1: </b> Test\n<b>player2: </b>Test"))), title="Chat")


    def input_area(self) -> TextArea:
        """Returns a TextWindow to use as the input field"""
        input_type = "GAME"
        return TextArea(height=1,
                        prompt=HTML(f"<style bg='darkcyan'>[{input_type}] $ </style>"),
                        style="class:input-field",
                        multiline=False,
                        wrap_lines=True,
                        focus_on_click=True)


    def __pt_container__(self) -> Container:
        """Returns the window container use"""
        return self.window
