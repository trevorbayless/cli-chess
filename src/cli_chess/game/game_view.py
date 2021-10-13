from cli_chess.game import GamePresenter

from prompt_toolkit.widgets import TextArea, Label, Button, Dialog
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.application import get_app


class GameView:
    """This is what the user sees. All ui input should go to the presenter directly"""
    def __init__(self, presenter):
        self.presenter = presenter
        self.make_move_button = Button(text="Make Move", handler=self.presenter.make_move)
        self.move_input = self.create_move_input()
        self.status_label = Label(text="Default", dont_extend_height=True)
        self.dialog = self.create_dialog()


    def create_move_input(self) -> TextArea:
        move_input = TextArea(height=1,
                            prompt=HTML(f"<style bg='darkcyan'>[GAME] $ </style>"),
                            style="class:input-field",
                            multiline=False,
                            wrap_lines=True,
                            focus_on_click=True)
        return move_input


    def get_move_input_text(self) -> str:
        return self.move_input.text


    def set_status_text(self, status_text) -> None:
        self.status_label.text = status_text


    def create_dialog(self) -> Dialog:
        """Create the Dialog wrapper"""
        return Dialog(title="Game view",
                      body=HSplit(
                          [
                            Label(text="This is the game view", dont_extend_height=True),
                            self.move_input,
                            self.status_label
                          ],
                          padding=D(preferred=1, max=1),
                      ),
                      buttons=[self.make_move_button],
                      with_background=True)


    def __pt_container__(self) -> Dialog:
        """Returns the dialog for container use"""
        return self.dialog


# class BoardDisplay:
#     def __init__(self):
#         pass


# class MoveListDisplay:
#     def __init__(self):
#         pass


# class ChatDisplay:
#     def __init__(self):
#         pass


# class InputField:
#     def __init__(self):
#         pass


# class GameDisplay:
#     def __init__(self):
#         pass


# class OnlineGameDisplay(GameDisplay):
#     def __init__(self, game_id):
#         self.game_id = game_id




# #!/usr/bin/env python
# from prompt_toolkit.application import Application
# from prompt_toolkit.formatted_text import HTML
# from prompt_toolkit.key_binding import KeyBindings
# from prompt_toolkit.styles import Style
# from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
# from prompt_toolkit.layout.dimension import D
# from prompt_toolkit.layout.layout import Layout
# from prompt_toolkit.buffer import Buffer
# from prompt_toolkit.layout.containers import (
#     HSplit,
#     VerticalAlign,
#     VSplit,
#     Window,
#     WindowAlign,
#     HorizontalAlign,
#     Float,
#     FloatContainer,
# )
# from prompt_toolkit.widgets import (
#     Box,
#     Button,
#     Checkbox,
#     Dialog,
#     Frame,
#     Label,
#     MenuContainer,
#     MenuItem,
#     ProgressBar,
#     RadioList,
#     TextArea,
# )

# ####
# ####
# #### NOTES: "text_editor.py" has some very good examples for what's trying to be achieved.
# ####
# ####

# from cli_chess import Board

# white_title = "BOT"
# white_id = "trevorbayless"#"ThisIsTheLongestName"
# white_rating = "1200"
# black_title = "GM"
# black_id = "DrNykterstein"
# black_rating = "3150"
# game_id = "McCH7dqI"
# game_status = "In progress"

# def display_turn() -> Window:
#     """Returns a window with who's turn it is to move"""
#     return Window(FormattedTextControl(HTML("<style bg='black' fg='white'><b> BLACK TO MOVE  </b></style>")), align=WindowAlign.CENTER)

# def board_display_window() -> Window:
#     """Returns a window with the current game"""
#     board = Board("black", "Standard", "rnbqkbnr/ppp2ppp/4p3/1B1p4/3P4/4P3/PPP2PPP/RNBQK1NR b KQkq - 1 3")
#     return Window(FormattedTextControl(HTML(board.board_display)), align=WindowAlign.CENTER, height=9, width=25)


# def display_whites_data() -> Window:
#     return Window(FormattedTextControl(HTML(f"<style fg='orangered'><b>{white_title}</b></style> {white_id} ({white_rating})")), height=1)


# def display_blacks_data() -> Window:
#     return Window(FormattedTextControl(HTML(f"<style fg='orangered'><b>{black_title}</b></style> {black_id} ({black_rating})")), height=1)


# def move_list_display() -> TextArea:
#     """Returns a TextWindow with the current move list"""
#     return TextArea("e4     ♞ f6\nd3     ♜ b2\nO-O-O  ♛ f6\nd3     ♜ b2#\ne4     ♞ f6\nd3     ♜ b2\nO-O-O  ♛ f6\nd3     ♜ b2#\ne4     ♞ f6\nd3     ♜ b2\nO-O-O  ♛ f6\nd3     ♜ b2#",
#                     line_numbers=True,
#                     height=6,
#                     read_only=True,
#                     focus_on_click=True,
#                     scrollbar=True,
#                     wrap_lines=False)

# def chat_display() -> Window:
#     return Frame(Window(FormattedTextControl(HTML(f"<b>{white_id}: </b> Good luck.\n<b>{black_id}: </b>Thanks, you too."))),
#                  title="Chat")


# def input_field_display() -> TextArea:
#     """Returns a TextWindow to use as the input field"""
#     input_type = "GAME"
#     return TextArea(height=1,
#                     prompt=HTML(f"<style bg='darkcyan'>[{input_type}] $ </style>"),
#                     style="class:input-field",
#                     multiline=False,
#                     wrap_lines=True,
#                     focus_on_click=True)


# def test_layout():
#     """Gets the layout to use when in game"""
#     dialog_body = HSplit(
#         [
#             VSplit(
#                 [
#                     HSplit(
#                         [
#                             display_turn(),
#                             board_display_window()
#                         ], align=VerticalAlign.TOP
#                     ),

#                     HSplit(
#                         [
#                             display_whites_data(),
#                             move_list_display(),
#                             display_blacks_data()
#                         ], align=VerticalAlign.CENTER
#                     ),
#                 ], align=HorizontalAlign.CENTER
#             ),
#             chat_display(),
#             input_field_display()
#         ]
#     )

#     return Dialog(body=dialog_body,
#                   title = "lichess.org/gFxcDgH",
#                   with_background=True, width=D(max=60, preferred=60))

# def get_in_game_layout():
#     return Layout(
#         FloatContainer(
#             content=test_layout(),
#             floats=[
#                 Float(
#                     Window(FormattedTextControl(HTML(f"Accept <b>draw?</b>")), height=2, style="bg:darkcyan fg:black"),
#                     bottom=0,
#                     right=3,
#                 ),
#                 # # Center float
#                 # Float(
#                 #     Frame(
#                 #         Window(FormattedTextControl(HTML(f"Are you <b>sure</b> you want to resign?</b>")), width=10, height=2, style="bg:#44ffff #ffffff"),
#                 #     )
#                 # ),
#                 # # Status bar float
#                 # Float(
#                 #     Window(FormattedTextControl("Bottom"), height=1, style="bg:#44ffff #ffffff"),
#                 #     bottom=0,
#                 # ),
#             ],
#         )
#     )


# kb = KeyBindings()

# @kb.add("c-c")
# def _(event):
#     event.app.exit()

# # Main style
# style = Style(
#     [
#         ("output-field", "bg:#000044 #ffffff"),
#         ("input-field", "bg:#000000 #ffffff"),
#         ("line", "#004400"),
#     ]
# )