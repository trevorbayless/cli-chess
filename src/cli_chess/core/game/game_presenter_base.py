from __future__ import annotations
from cli_chess.core.game import GameViewBase, PlayableGameViewBase
from cli_chess.modules.board import BoardPresenter
from cli_chess.modules.move_list import MoveListPresenter
from cli_chess.modules.material_difference import MaterialDifferencePresenter
from cli_chess.modules.player_info import PlayerInfoPresenter
from cli_chess.modules.clock import ClockPresenter
from cli_chess.modules.premove import PremovePresenter
from cli_chess.utils import log, AlertType, RequestSuccessfullySent, EventTopics, save_game_pgn
from cli_chess.utils.config import game_config
from cli_chess.utils.move_input_preview import analyze_move_input, longest_matching_san_prefix
from abc import ABC, abstractmethod
import chess
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.game import GameModelBase, PlayableGameModelBase
    from prompt_toolkit.buffer import Buffer


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
        self._move_input_hint_text = ""

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
            self._save_pgn()

    def on_move_input_changed(self, text: str) -> None:
        """Refresh live board hints and the move preview line while typing."""
        self._refresh_move_input_preview(text)

    def get_move_input_hint_text(self) -> str:
        """Resolved SAN when input matches exactly one legal move (for the hint line)."""
        return self._move_input_hint_text

    def try_tab_complete_move_input(self, buffer: "Buffer") -> bool:
        """Extend partial SAN to the longest common prefix of matching moves. Returns True if applied."""
        if not game_config.get_boolean(game_config.Keys.LIVE_MOVE_INPUT_HIGHLIGHTS):
            return False
        if not game_config.get_boolean(game_config.Keys.LIVE_MOVE_INPUT_AUTOCOMPLETE):
            return False
        if self.model.board_model.is_game_over():
            return False

        current = buffer.text.strip()
        if not current or current.lower().startswith("send"):
            return False

        board = self.model.board_model.board
        next_prefix = longest_matching_san_prefix(board, current)
        if not next_prefix or next_prefix == current:
            return False

        buffer.text = next_prefix
        buffer.cursor_position = len(next_prefix)
        return True

    def _refresh_move_input_preview(self, text: str) -> None:
        self._move_input_hint_text = ""
        board_model = self.model.board_model

        if not game_config.get_boolean(game_config.Keys.LIVE_MOVE_INPUT_HIGHLIGHTS):
            board_model.clear_move_input_highlights()
            return

        if board_model.is_game_over():
            board_model.clear_move_input_highlights()
            return

        stripped = text.strip()
        if not stripped:
            board_model.clear_move_input_highlights()
            return

        if stripped.lower().startswith("send"):
            board_model.clear_move_input_highlights()
            return

        analysis = analyze_move_input(board_model.board, stripped)
        if not analysis.from_squares:
            board_model.clear_move_input_highlights()
            return

        show_targets = game_config.get_boolean(game_config.Keys.LIVE_MOVE_INPUT_SHOW_TARGETS)

        if analysis.preview_move:
            board_model.set_move_input_highlights(
                set(),
                set(),
                analysis.preview_move,
            )
            self._move_input_hint_text = (
                f"If you press Enter: {board_model.board.san(analysis.preview_move)}"
            )
        else:
            to_sq = set(analysis.to_squares) if show_targets else set()
            board_model.set_move_input_highlights(set(analysis.from_squares), to_sq, chess.Move.null())

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
            elif inpt_lower.find("send") == 0:
                self.post_message(inpt.replace("send", "", 1))
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

    def post_message(self, text: str) -> None:
        """Send message to opponent"""
        try:
            self.model.post_message(text)
        except Exception as e:
            self.view.alert.show_alert(str(e))

    def is_game_in_progress(self) -> bool:
        return self.model.game_in_progress

    @abstractmethod
    def _parse_and_present_game_over(self) -> str:
        pass

    def _save_pgn(self) -> None:
        """Save PGN to save locaton and print path on screen"""
        try:
            is_online = self.model.game_metadata.game_id is not None
            path = save_game_pgn(self.model.board_model, self.model.game_metadata, is_online=is_online)
            if path:
                existing = self.view.alert._alert_label.text or ""
                self.view.alert._alert_label.text = f"{existing}\nGame saved: {path}" if existing else f"Game saved: {path}"
        except Exception as e:
            log.error(f"Unexpected error saving PGN: {e}")
