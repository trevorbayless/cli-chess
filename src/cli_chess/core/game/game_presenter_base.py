from __future__ import annotations
from cli_chess.core.game import GameViewBase, PlayableGameViewBase
from cli_chess.modules.board import BoardPresenter
from cli_chess.modules.move_list import MoveListPresenter
from cli_chess.modules.material_difference import MaterialDifferencePresenter
from cli_chess.modules.player_info import PlayerInfoPresenter
from cli_chess.modules.clock import ClockPresenter
from cli_chess.modules.premove import PremovePresenter
from cli_chess.utils import log, AlertType, RequestSuccessfullySent, EventTopics
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase, PlayableGameModelBase


class GamePresenterBase(ABC):
    def __init__(self, model: GameModelBase):
        self.model = model
        self.board_presenter = BoardPresenter(model.board_model)
        self.move_list_presenter = MoveListPresenter(model.move_list_model)
        self.material_diff_presenter = MaterialDifferencePresenter(model.material_diff_model)
        self.player_info_presenter = PlayerInfoPresenter(model)
        self.clock_presenter = ClockPresenter(model)
        self.view = self._get_view()

        self.model.e_game_model_updated.add_listener(self.update)
        log.debug(f"Created {type(self).__name__} (id={id(self)})")

    @abstractmethod
    def _get_view(self) -> GameViewBase:
        """Returns the view to use for this presenter"""
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Listens to game model updates when notified.
           See model for specific kwargs that are currently being sent.
        """
        if EventTopics.GAME_START in args:
            self.view.alert.clear_alert()

    def flip_board(self) -> None:
        """Flip the board orientation"""
        self.model.board_model.set_board_orientation(not self.model.board_model.get_board_orientation())

    def exit(self) -> None:
        """Exit current presenter/view"""
        log.debug("Exiting game presenter")
        self.model.cleanup()
        self.view.exit()


class PlayableGamePresenterBase(GamePresenterBase, ABC):
    def __init__(self, model: PlayableGameModelBase):
        self.premove_presenter = PremovePresenter(model.premove_model)
        super().__init__(model)
        self.model = model

    @abstractmethod
    def _get_view(self) -> PlayableGameViewBase:
        """Returns the view to use for this presenter"""
        return PlayableGameViewBase(self)

    @abstractmethod
    def is_vs_ai(self) -> bool:
        """Inheriting classes must specify if the game
           is versus AI (offline engine or Lichess)
        """
        pass

    def update(self, *args, **kwargs) -> None:
        """Update method called on game model updates. Overrides base."""
        super().update(*args, **kwargs)
        if EventTopics.MOVE_MADE in args:
            self.view.alert.clear_alert()
        if EventTopics.GAME_END in args:
            self._parse_and_present_game_over()
            self.premove_presenter.clear_premove()

    def user_input_received(self, inpt: str) -> None:
        """Respond to the users input. This input can either be the
           move input, or game actions (such as resign)
        """
        try:
            inpt_lower = inpt.lower()
            if inpt_lower == "resign" or inpt_lower == "quit" or inpt_lower == "exit":
                self.resign()
            elif inpt_lower == "draw" or inpt_lower == "offer draw":
                self.offer_draw()
            elif inpt_lower == "takeback" or inpt_lower == "back" or inpt_lower == "undo":
                self.propose_takeback()
            elif self.model.is_my_turn():
                self.make_move(inpt)
            else:
                self.model.set_premove(inpt)
        except Exception as e:
            self.view.alert.show_alert(str(e))

    def make_move(self, move: str) -> None:
        """Make the passed in move on the board"""
        try:
            move = move.strip()
            if move:
                self.model.make_move(move)
        except Exception as e:
            self.view.alert.show_alert(str(e))

    def propose_takeback(self) -> None:
        """Proposes a takeback"""
        try:
            self.model.propose_takeback()
        except Exception as e:
            if isinstance(e, RequestSuccessfullySent):
                self.view.alert.show_alert(str(e), AlertType.NEUTRAL)
            else:
                self.view.alert.show_alert(str(e))

    def offer_draw(self) -> None:
        """Offers a draw"""
        try:
            self.model.offer_draw()
        except Exception as e:
            if isinstance(e, RequestSuccessfullySent):
                self.view.alert.show_alert(str(e), AlertType.NEUTRAL)
            else:
                self.view.alert.show_alert(str(e))

    def resign(self) -> None:
        """Resigns the game"""
        try:
            if self.model.game_in_progress:
                self.model.resign()
            else:
                self.exit()
        except Exception as e:
            self.view.alert.show_alert(str(e))

    def is_game_in_progress(self) -> bool:
        return self.model.game_in_progress

    @abstractmethod
    def _parse_and_present_game_over(self) -> str:
        pass
