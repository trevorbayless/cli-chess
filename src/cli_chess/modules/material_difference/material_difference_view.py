from __future__ import annotations
from prompt_toolkit.layout import Container, ConditionalContainer, Window, HSplit, D
from prompt_toolkit.filters import to_filter
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.material_difference import MaterialDifferencePresenter


class MaterialDifferenceView:
    def __init__(self, presenter: MaterialDifferencePresenter, initial_diff: str, show: bool = True):
        self.presenter = presenter
        self.show = show
        self._diff_text_area = TextArea(text=initial_diff,
                                        style="class:material-difference",
                                        width=D(min=1),
                                        height=D(max=1),
                                        read_only=True,
                                        focusable=False,
                                        multiline=False,
                                        wrap_lines=False)
        self._container = self._create_container()

    def _create_container(self):
        """Creates the container for the material difference. Handles providing
           an empty container if the view should be hidden. This allows for
           the container display formatting to remain consistent
        """
        return HSplit([
            ConditionalContainer(self._diff_text_area, to_filter(self.show)),
            ConditionalContainer(Window(height=D(max=1)), to_filter(not self.show))
        ])

    def update(self, difference: str) -> None:
        """Updates the view output with the passed in text"""
        self._diff_text_area.text = difference

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
