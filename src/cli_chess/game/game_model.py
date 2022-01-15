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

from cli_chess.game.board import BoardModel
from cli_chess.game.move_list import MoveListModel
from cli_chess.game.material_difference import MaterialDifferenceModel
from cli_chess.game.offline.engine import EngineModel


class GameModel:
    def __init__(self):
        self.board_model = BoardModel()
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)


class OfflineGameModel(GameModel):
    def __init__(self):
        super().__init__()
        self.engine_model = EngineModel(self.board_model)
