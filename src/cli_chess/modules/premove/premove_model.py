from cli_chess.modules.board import BoardModel
from cli_chess.utils import EventManager, EventTopics, log
from chess import Move, InvalidMoveError, IllegalMoveError, AmbiguousMoveError


class PremoveModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)
        self.premove = ""

        self._event_manager = EventManager()
        self.e_premove_model_updated = self._event_manager.create_event()

    def update(self, *args, **kwargs) -> None: # noqa
        """Updates the premove model based on board updates"""
        if EventTopics.GAME_END in args:
            self.clear_premove()

    def pop_premove(self) -> str:
        """Returns the set premove, but also clears it after"""
        premove = self.premove
        if premove:
            log.debug(f"Popping premove: {self.premove}")
            self.clear_premove()
        return premove

    def clear_premove(self) -> None:
        """Clears the set premove"""
        self.premove = ""
        self.board_model.clear_premove_highlight()
        self._notify_premove_model_updated()

    def set_premove(self, move: str = None) -> None:
        """Sets the passed in move as the premove to make.
           Raises an exception if the premove is invalid.
        """
        try:
            premove = self._validate_premove(move)
            self.premove = move
            log.debug(f"Premove set to ({move})")
            self.board_model.set_premove_highlight(premove)
        except Exception as e:
            raise e

        self._notify_premove_model_updated()

    def _validate_premove(self, move: str = None) -> Move:
        """Checks if the premove passed in is valid in the context of game.
           Raises an exception if the premove is invalid. Returns the move
           in the format of chess.Move
        """
        try:
            if not move:
                raise Warning("No move specified")

            if self.premove:
                raise Warning("You already have a premove set")

            tmp_premove_board = self.board_model.board.copy(stack=False)
            tmp_premove_board.turn = not tmp_premove_board.turn
            try:
                return tmp_premove_board.push_san(move.strip())

            except Exception as e:
                if isinstance(e, InvalidMoveError):
                    raise ValueError(f"Invalid premove: {move}")
                elif isinstance(e, IllegalMoveError):
                    raise ValueError(f"Illegal premove: {move}")
                elif isinstance(e, AmbiguousMoveError):
                    raise ValueError(f"Ambiguous premove: {move}")
                else:
                    raise e
        except Exception:
            raise

    def _notify_premove_model_updated(self) -> None:
        """Notifies listeners of premove model updates"""
        self.e_premove_model_updated.notify()

    def cleanup(self) -> None:
        """Handles model cleanup tasks. This should only ever
           be run when this model is no longer needed.
        """
        self._event_manager.purge_all_events()
