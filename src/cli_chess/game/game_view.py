from __future__ import annotations
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.layout.containers import Container, HSplit, VSplit
from prompt_toolkit.buffer import BufferAcceptHandler
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.layout import Layout

from cli_chess.game.board import BoardView
from cli_chess.game.move_list import MoveListView
from cli_chess.game.material_difference import MaterialDifferenceView


class GameView:
    def __init__(self, game_presenter: GamePresenter, board_view: BoardView, move_list_view: MoveListView,
                       material_diff_white_view: MaterialDifferenceView, material_diff_black_view: MaterialDifferenceView):
        self.game_presenter = game_presenter
        self.board_output_container = board_view
        self.move_list_container = move_list_view
        self.material_diff_white_container = material_diff_white_view
        self.material_diff_black_container = material_diff_black_view
        self.input_field_container = self._create_input_field_container()
        self.container = self._create_container()
        get_app().layout = Layout(self.container, self.input_field_container)


    def _create_container(self) -> Container:
        return HSplit(
            [
                VSplit(
                    [
                        self.board_output_container,
                        HSplit(
                            [
                                self.material_diff_black_container,
                                self.move_list_container,
                                self.material_diff_white_container,
                            ])
                    ], window_too_small=self.board_output_container),
                self.input_field_container
            ]
        )


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


    def _accept_input(self, input: BufferAcceptHandler):
        """The accept handler for the input field"""
        if input.text == "quit":
            get_app().exit()
        else:
            self.game_presenter.input_received(input.text)
            self.input_field_container.text = ''


    def __pt_container__(self) -> Container:
        """Returns this container"""
        return self.container
