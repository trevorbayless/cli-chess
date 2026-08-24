from __future__ import annotations
from cli_chess.modules.game_input_field import GameInputView
from cli_chess.utils import log
from cli_chess.utils.config import game_config
from cli_chess.utils.move_input_preview import analyze_move_input, longest_matching_san_prefix
from chess import Move
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from cli_chess.modules.game_input_field import GameInputModel

class GameInputPresenter:
    def __init__(self, model: GameInputModel, show_alert_callback: Callable[[str], None] | None = None):
        self.model = model
        self.view = GameInputView(self)
        self.cb_show_alert: Callable[[str], None] | None = show_alert_callback

    # TODO: I don't think I like the hard coded keywords... maybe have this ask
    #       the individual models if they have a word they know that was entered
    #       and return a function pointer to call here?

    # TODO: The problem here with the engine not moving was that I was calling the models
    #       make_move - instead of the presenters. I believe what I need to do is create a model
    #       for this game_input, which then emits an event on chat input. Then, anyone interested
    #       in chat input can subscribe (the models), and then broadcast back to the necessary presenter.
    #       This kind of goes hand in hand with the above comment as well.
    def input_received(self, inpt: str) -> None:
        """Respond to the users input. This input can either be the
           move input, game actions (such as resign), chat, etc
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
            elif self.is_my_turn():
                self.make_move(inpt)
            else:
                self.set_premove(inpt)
        except Exception as e:
            if self.cb_show_alert:
                self.cb_show_alert(str(e))
            else:
                log.error(f"Alert callback missing - Unable to show alert with text ${str(e)}")

    def on_move_input_changed(self, text: str) -> None:
        """Refresh live board hints and the move preview line while typing."""
        self._refresh_move_input_preview(text)

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

    # TODO: This whole function should likely be split up. Have move input hint
    #       rendered here, and logic for square highlighting of the hint done
    #       from the board model. Have this class then register with an update
    #       callback with returned move inputs?
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
                f"Tab to accept: {board_model.board.san(analysis.preview_move)}"
            )
        else:
            to_sq = set(analysis.to_squares) if show_targets else set()
            board_model.set_move_input_highlights(set(analysis.from_squares), to_sq, Move.null())
