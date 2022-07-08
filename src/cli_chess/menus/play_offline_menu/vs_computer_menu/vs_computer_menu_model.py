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

from cli_chess.menus import OfflineGameOptions


class VsComputerMenuModel:
    def __init__(self):
        self.questions = [
            {
                "type": "select",
                "name": "variant",
                "message": "Select the variant",
                "instruction": " ",
                "choices": [option for option in OfflineGameOptions.variant_options_dict],
                "use_shortcuts": True,
                "use_jk_keys": True,
            },
            {
                "type": "select",
                "name": "time_control",
                "message": "Select the time control",
                "instruction": " ",
                "choices": [option for option in OfflineGameOptions.time_control_options_dict],
                "use_shortcuts": True,
                "use_jk_keys": True,
            },
            {
                "type": "select",
                "name": "strength",
                "message": "Select the computers strength",
                "instruction": " ",
                "choices": [option for option in OfflineGameOptions.skill_level_options_dict],
                "use_shortcuts": True,
                "use_jk_keys": True,
            },
            {
                "type": "select",
                "name": "color",
                "message": "Select the color to play as",
                "instruction": " ",
                "choices": [option for option in OfflineGameOptions.color_options_dict],
                "use_shortcuts": True,
                "use_jk_keys": True,
            },
        ]

    def get_questions(self):
        """Returns the dictionary of questions"""
        return self.questions
