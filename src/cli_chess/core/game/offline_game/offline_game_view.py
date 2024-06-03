from __future__ import annotations
from cli_chess.core.game import PlayableGameViewBase
from prompt_toolkit.layout import Container, HSplit, VSplit, VerticalAlign
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game.offline_game import OfflineGamePresenter


class OfflineGameView(PlayableGameViewBase):
    def __init__(self, presenter: OfflineGamePresenter):
        self.presenter = presenter
        super().__init__(presenter)

    def _create_container(self) -> Container:
        main_content = Box(
            HSplit([
                VSplit([
                    self.board_output_container,
                    Box(HSplit([
                        self.player_info_upper_container,
                        self.material_diff_upper_container,
                        self.move_list_container,
                        self.material_diff_lower_container,
                        self.player_info_lower_container,
                    ]), padding=0, padding_top=1)
                ]),
                self.input_field_container,
                self.premove_container,
                self.alert,
            ]),
            padding=0
        )
        function_bar = HSplit([
            self._create_function_bar()
        ], align=VerticalAlign.BOTTOM)

        return HSplit([main_content, function_bar], key_bindings=self.get_key_bindings())
