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
from cli_chess.modules.premove import PremoveView
from chess import Color, COLOR_NAMES
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase


class PremovePresenter:
    def __init__(self, model: GameModelBase):
        self.model = model

        self.view = PremoveView(self, self.get_permove())

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Updates the view based on specific model updates"""
        self.view.update(self.get_permove())

    def get_permove(self) -> dict:
        return self.model.board_model.get_premove()
