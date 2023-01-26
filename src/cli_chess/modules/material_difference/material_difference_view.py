# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
from prompt_toolkit.layout import ConditionalContainer, D
from prompt_toolkit.filters import to_filter
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.material_difference import MaterialDifferencePresenter


class MaterialDifferenceView:
    def __init__(self, presenter: MaterialDifferencePresenter, initial_diff: str, show: bool = True):
        self.presenter = presenter
        self._diff_text_area = TextArea(text=initial_diff,
                                        style="class:material-difference",
                                        width=D(min=1),
                                        height=D(min=1, max=1),
                                        read_only=True,
                                        focusable=False,
                                        multiline=False,
                                        wrap_lines=False)
        self.show = show

    def update(self, difference: str) -> None:
        """Updates the view output with the passed in text"""
        self._diff_text_area.text = difference

    def __pt_container__(self) -> ConditionalContainer:
        """Returns this views container"""
        return ConditionalContainer(self._diff_text_area, to_filter(self.show))
