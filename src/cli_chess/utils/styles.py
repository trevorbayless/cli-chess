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

light_piece_color = "white"
dark_piece_color = "black"

default = {
    # Game styling
    "rank-label": "fg:gray",
    "file-label": "fg:gray",

    "light-square": "bg:cadetblue",
    "light-square.light-piece": f"fg:{light_piece_color}",
    "light-square.dark-piece": f"fg:{dark_piece_color}",

    "dark-square": "bg:darkslateblue",
    "dark-square.light-piece": f"fg:{light_piece_color}",
    "dark-square.dark-piece": f"fg:{dark_piece_color}",

    "last-move": "bg:yellowgreen",
    "last-move.light-piece": f"fg:{light_piece_color}",
    "last-move.dark-piece": f"fg:{dark_piece_color}",
    
    "pre-move": "bg:darkorange",
    "pre-move.light-piece": f"fg:{light_piece_color}",
    "pre-move.dark-piece": f"fg:{dark_piece_color}",

    "in-check": "bg:red",
    "in-check.light-piece": f"fg:{light_piece_color}",
    "in-check.dark-piece": f"fg:{dark_piece_color}",

    "material-difference": "fg:gray",
    "move-list": "fg:gray",
    "move-input": "fg:white bold",

    "player-info": "fg:white",
    "player-info.title": "fg:darkorange bold",
    "player-info.title.bot": "fg:darkmagenta",
    "player-info.pos-rating-diff": "fg:darkgreen",
    "player-info.neg-rating-diff": "fg:darkred",

    # Program styling
    "menu": "bg:",
    "menu.category-title": "fg:black bg:limegreen",
    "menu.option": "fg:white",
    "menu.multi-value": "fg:orangered",
    "focused-selected": "fg:black bg:mediumturquoise noinherit",
    "unfocused-selected": "fg:black bg:white noinherit",
    "menu.multi-value focused-selected": "fg:orangered bold noinherit",
    "menu.multi-value unfocused-selected": "fg:orangered noinherit",

    "function-bar.key": "fg:white",
    "function-bar.label": "fg:black bg:mediumturquoise",
    "function-bar.spacer": "",

    "label": "fg:white",
    "label.dim": "fg:dimgray",
    "label.success": "fg:darkgreen",
    "label.error": "fg:darkred",
    "label.success.banner": "bg:darkgreen fg:white",
    "label.error.banner": "bg:darkred fg:white",
    "label.neutral.banner": "bg:slategray fg:white",

    "text-area.input": "fg:orangered bold",
    "text-area.input.placeholder": "italic",
    "text-area.prompt": "fg:white bg:darkcyan bold noinherit",

    "validation-toolbar": "fg:white bg:darkred",
}
