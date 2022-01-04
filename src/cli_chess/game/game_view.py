from prompt_toolkit import HTML
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.layout.containers import Container, HSplit, VSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.layout import Layout


class GameView:
    def __init__(self, game_presenter, board_view, move_list_view,
                 material_diff_white, material_diff_black):
        self.game_presenter = game_presenter
        self.board_output_container = board_view
        self.move_list_container = move_list_view
        self.material_diff_white_container = material_diff_white
        self.material_diff_black_container = material_diff_black
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


    def _accept_input(self, input):
        """The accept handler for the input field"""
        if input.text == "quit":
            get_app().exit()
        else:
            self.game_presenter.input_received(input.text)
            self.input_field_container.text = ''


    def __pt_container__(self) -> Container:
        """Returns this container"""
        return self.container
