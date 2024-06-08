from cli_chess.modules.board import BoardModel
from cli_chess.modules.move_list import MoveListModel
from cli_chess.modules.material_difference import MaterialDifferenceModel
from cli_chess.modules.premove import PremoveModel
from cli_chess.utils import EventManager, log
from .game_metadata import GameMetadata
from chess import Color, WHITE, COLOR_NAMES
from random import getrandbits
from abc import ABC, abstractmethod


class GameModelBase:
    def __init__(self, orientation: Color = WHITE, variant="standard", fen=""):
        self.game_metadata = GameMetadata()

        self.board_model = BoardModel(orientation, variant, fen)
        self.move_list_model = MoveListModel(self.board_model)
        self.material_diff_model = MaterialDifferenceModel(self.board_model)

        self._event_manager = EventManager()
        self.e_game_model_updated = self._event_manager.create_event()
        self.board_model.e_board_model_updated.add_listener(self.update)

        # Keep track of all associated models to handle bulk cleanup on exit
        self._assoc_models = [self.board_model, self.move_list_model, self.material_diff_model]

        log.debug(f"Created {type(self).__name__} (id={id(self)})")

    def update(self, *args, **kwargs) -> None:
        """Called automatically as part of an event listener. This method
           listens to subscribed model update events and if deemed necessary
           triages and notifies listeners of the event.
        """
        self._notify_game_model_updated(*args, **kwargs)

    def cleanup(self) -> None:
        """Cleans up after this model by clearing all associated models event listeners.
           This should only ever be run when the models are no longer needed.
        """
        self._event_manager.purge_all_events()

        # Notify associated models to clean up
        for model in self._assoc_models:
            try:
                model.cleanup()
                log.debug(f"Finished cleaning up after {type(model).__name__} (id={id(model)})")
            except AttributeError:
                log.error(f"{type(model).__name__} does not have a cleanup method")

    def _notify_game_model_updated(self, *args, **kwargs) -> None:
        """Notify listeners that the model has updated"""
        self.e_game_model_updated.notify(*args, **kwargs)


class PlayableGameModelBase(GameModelBase, ABC):
    def __init__(self, play_as_color: str, variant="standard", fen=""):
        self.my_color = self._get_side_to_play_as(play_as_color)
        self.game_in_progress = False

        super().__init__(orientation=self.my_color, variant=variant, fen=fen)
        self.premove_model = PremoveModel(self.board_model)
        self._assoc_models = self._assoc_models + [self.premove_model]

    def is_my_turn(self) -> bool:
        """Return True if it's our turn"""
        return self.board_model.get_turn() == self.my_color

    @staticmethod
    def _get_side_to_play_as(color: str) -> Color:
        """Returns a chess.Color based on the color string passed in. If the color string
           is unmatched, a random value of chess.WHITE or chess.BLACK will be returned
        """
        if color.lower() in COLOR_NAMES:
            return Color(COLOR_NAMES.index(color))
        else:  # Get random color to play as
            return Color(getrandbits(1))

    @abstractmethod
    def make_move(self, move: str) -> None:
        pass

    @abstractmethod
    def set_premove(self, move) -> None:
        pass

    @abstractmethod
    def propose_takeback(self) -> None:
        pass

    @abstractmethod
    def offer_draw(self) -> None:
        pass

    @abstractmethod
    def resign(self) -> None:
        pass
