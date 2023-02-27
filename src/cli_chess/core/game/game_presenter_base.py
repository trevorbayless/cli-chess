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
from cli_chess.core.game import GameViewBase, PlayableGameViewBase
from cli_chess.modules.board import BoardPresenter
from cli_chess.modules.move_list import MoveListPresenter
from cli_chess.modules.material_difference import MaterialDifferencePresenter
from cli_chess.modules.player_info import PlayerInfoPresenter
from cli_chess.utils.logging import log
from chess import Color, COLOR_NAMES
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase, PlayableGameModelBase


class GamePresenterBase:
    def __init__(self, model: GameModelBase):
        self.model = model
        self.board_presenter = BoardPresenter(model.board_model)
        self.move_list_presenter = MoveListPresenter(model.move_list_model)
        self.material_diff_presenter = MaterialDifferencePresenter(model.material_diff_model)
        self.player_info_presenter = PlayerInfoPresenter(model)
        self.view = GameViewBase(self)

        self.model.e_game_model_updated.add_listener(self.update)

    def update(self, **kwargs) -> None:
        """Listens to game model updates when notified. Child classes should
           override if interested in specific kwargs. See model for specific
           kwargs that are currently being sent.
        """
        pass

    def flip_board(self) -> None:
        """Flip the board orientation"""
        self.model.board_model.set_board_orientation(not self.model.board_model.get_board_orientation())

    def exit(self) -> None:
        """Exit current presenter/view"""
        self.view.exit()


class PlayableGamePresenterBase(GamePresenterBase):
    def __init__(self, model: PlayableGameModelBase):
        self.model = model
        super().__init__(model)
        self.view = PlayableGameViewBase(self)

        self.model.board_model.e_successful_move_made.add_listener(self.view.clear_error)

    def update(self, **kwargs) -> None:
        """Overrides base and responds to specific model updates"""
        if 'gameOver' in kwargs:
            self._parse_and_present_game_over()

    def _parse_and_present_game_over(self):
        """Handles parsing and presenting the game over status"""
        if not self.is_game_in_progress():
            status = self.model.game_metadata['state']['status']
            winner = self.model.game_metadata['state']['winner'].capitalize()

            status_win_reasons = ['mate', 'resign', 'timeout', 'outoftime', 'cheat', 'variantEnd']
            if winner and status in status_win_reasons:
                output = f" • {winner} is victorious"
                loser = COLOR_NAMES[not Color(COLOR_NAMES.index(winner.lower()))].capitalize()

                if status == "mate":
                    output = "Checkmate" + output
                elif status == "resign":
                    output = f"{loser} resigned" + output
                elif status == "timeout":
                    output = f"{loser} left the game" + output
                elif status == "outoftime":
                    output = f"{loser} time out" + output
                elif status == "cheat":
                    output = "Cheat detected"
                else:  # TODO: Handle variantEnd (need to know variant)
                    log.debug(f"PlayableGamePresenterBase: Received game over with uncaught status: {status} / {winner}")
                    output = "Game over" + output

            else:  # Handle other game end reasons
                if status == "aborted":
                    output = "Game aborted"
                elif status == "draw":
                    output = "Game over • Draw"
                elif status == "stalemate":
                    output = "Game over • Stalemate"
                else:
                    log.debug(f"PlayableGamePresenterBase: Received game over with uncaught status: {status}")
                    output = "Game over"

            self.view.show_error(output)

    def user_input_received(self, inpt: str) -> None:
        """Respond to the users input. This input can either be the
           move input, or game actions (such as resign)
        """
        inpt_lower = inpt.lower()
        if inpt_lower == "resign" or inpt_lower == "quit" or inpt_lower == "exit":
            self.resign()
        elif inpt_lower == "draw" or inpt_lower == "offer draw":
            self.offer_draw()
        elif inpt_lower == "takeback" or inpt_lower == "back" or inpt_lower == "undo":
            self.propose_takeback()
        else:
            self.make_move(inpt)

    def make_move(self, move: str) -> None:
        """Make the passed in move on the board"""
        try:
            move = move.strip()
            if move:
                self.model.make_move(move)
                self.view.clear_error()
        except Exception as e:
            self.view.show_error(f"{e}")

    def propose_takeback(self) -> None:
        """Proposes a takeback"""
        try:
            self.model.propose_takeback()
        except Exception as e:
            self.view.show_error(f"{e}")

    def offer_draw(self) -> None:
        """Offers a draw"""
        try:
            self.model.offer_draw()
        except Exception as e:
            self.view.show_error(f"{e}")

    def resign(self) -> None:
        """Resigns the game"""
        try:
            if self.model.game_in_progress:
                self.model.resign()
            else:
                self.exit()
        except Exception as e:
            self.view.show_error(f"{e}")

    def is_game_in_progress(self) -> bool:
        return self.model.game_in_progress
