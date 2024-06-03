from __future__ import annotations
from cli_chess.utils.ui_common import repaint_ui
from prompt_toolkit.layout import Window, FormattedTextControl, D
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.board import BoardPresenter


class BoardView:
    def __init__(self, presenter: BoardPresenter, initial_board_output: list):
        self.presenter = presenter
        self.board_output = FormattedTextControl(HTML(self._build_output(initial_board_output)))
        self._container = self._create_container()

    def _create_container(self):
        """Create the Board container"""
        return Box(Window(
            self.board_output,
            always_hide_cursor=True,
            width=D(max=18, preferred=18),
            height=D(max=9, preferred=9)
        ), padding=1)

    def _build_output(self, board_output_list: list) -> str:
        """Returns a string containing the board output to be used for
           display. The string returned will contain HTML elements"""
        board_output_str = ""

        for square in board_output_list:
            square_style = f"{square['square_display_color']}.{square['piece_display_color']}"
            piece_str = square['piece_str']
            piece_str += " " if square['piece_str'] else "  "

            board_output_str += f"<rank-label>{square['rank_label']}</rank-label>"
            board_output_str += f"<{square_style}>{piece_str}</{square_style}>"

            if square['is_end_of_rank']:
                board_output_str += "\n"

        file_labels = " " + self.presenter.get_file_labels()
        board_output_str += f"<file-label>{file_labels}</file-label>"

        return board_output_str

    def update(self, board_output_list: list):
        """Updates the board output with the passed in text"""
        self.board_output.text = HTML(self._build_output(board_output_list))
        repaint_ui()

    def __pt_container__(self) -> Box:
        """Returns this container"""
        return self._container
