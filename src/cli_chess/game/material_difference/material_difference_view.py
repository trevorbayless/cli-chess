# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.game.material_difference import MaterialDifferencePresenter


class MaterialDifferenceView:
    def __init__(self, material_diff_presenter: MaterialDifferencePresenter, initial_diff: str, show: bool = True):
        self.material_diff_presenter = material_diff_presenter
        self.difference_output = TextArea(text=initial_diff,
                                          width=D(min=1, max=20),
                                          height=D(min=1, max=1),
                                          read_only=True,
                                          focusable=False,
                                          multiline=False,
                                          wrap_lines=False)
        self.show = show
        self.root_container = ConditionalContainer(self.difference_output, show)

    def update(self, difference: str) -> None:
        """Updates the view output with the passed in text"""
        if self.show:
            self.difference_output.text = difference

    def __pt_container__(self) -> ConditionalContainer:
        """Returns this views container"""
        return self.root_container
