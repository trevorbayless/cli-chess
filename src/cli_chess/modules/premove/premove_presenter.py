# Copyright (C) 2021-2024 Trevor Bayless <trevorbayless1@gmail.com>
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
from cli_chess.modules.premove import PremoveView
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.premove import PremoveModel


class PremovePresenter:
    def __init__(self, model: PremoveModel):
        self.model = model
        self.view = PremoveView(self)
        self.model.e_premove_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        self.view.update(self.model.premove)

    def set_premove(self, move: str) -> None:
        if move:
            return self.model.set_premove(move)

    def pop_premove(self) -> str:
        """Returns the set premove, but also clears it after"""
        return self.model.pop_premove()

    def clear_premove(self) -> None:
        self.model.clear_premove()

    def is_premove_set(self) -> bool:
        """Returns True if a premove is set"""
        return bool(self.model.premove)
