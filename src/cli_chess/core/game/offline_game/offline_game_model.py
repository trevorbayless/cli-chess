from cli_chess.core.game import PlayableGameModelBase
from cli_chess.modules.engine import EngineModel
from cli_chess.core.game.game_options import GameOption
from cli_chess.utils import EventTopics, log
from cli_chess.utils.config import player_info_config
from chess import COLOR_NAMES
from typing import Optional, Dict


class OfflineGameModel(PlayableGameModelBase):
    def __init__(self, game_parameters: dict):
        super().__init__(play_as_color=game_parameters[GameOption.COLOR],
                         variant=game_parameters[GameOption.VARIANT])

        self.engine_model = EngineModel(self.board_model, game_parameters)
        self.game_in_progress = True
        self._update_game_metadata(EventTopics.GAME_PARAMS, data=game_parameters)

    def update(self, *args, **kwargs) -> None:
        """Called automatically as part of an event listener. This method
           listens to subscribed model update events and if deemed necessary
           triages and notifies listeners of the event.
        """
        super().update(*args, **kwargs)
        if EventTopics.GAME_END in args:
            self._report_game_over()

    def make_move(self, move: str):
        """Sends the move to the board model for it to be made"""
        if self.game_in_progress:
            try:
                if self.board_model.board.is_game_over():
                    self.game_in_progress = False
                    raise Warning("Game has already ended")

                if not self.is_my_turn():
                    raise Warning("Not your turn")

                self.board_model.make_move(move.strip())
                self.premove_model.clear_premove()

            except Exception:
                raise
        else:
            log.warning("Attempted to make a move in a game that's not in progress")
            raise Warning("Game has already ended")

    def set_premove(self, move: str) -> None:
        """Sets the premove"""
        self.premove_model.set_premove(move)

    def propose_takeback(self) -> None:
        """Take back the previous move"""
        try:
            if self.board_model.board.is_game_over():
                raise Warning("Game has already ended")

            self.premove_model.clear_premove()
            self.board_model.takeback(self.my_color)
        except Exception as e:
            log.error(f"Takeback failed - {e}")
            raise

    def offer_draw(self) -> None:
        raise Warning("Offline engine does not accept draw offers")

    def resign(self) -> None:
        """Handles resigning the game"""
        if self.game_in_progress:
            try:
                self.board_model.handle_resignation(self.my_color)
            except Exception:
                raise
        else:
            log.warning("Attempted to resign a game that's not in progress")
            raise Warning("Game has already ended")

    def _update_game_metadata(self, *args, data: Optional[Dict] = None, **kwargs) -> None:
        """Parses and saves the data of the game being played"""
        if not data:
            return
        try:
            if EventTopics.GAME_PARAMS in args:
                self.game_metadata.my_color = self.my_color
                self.game_metadata.variant = data[GameOption.VARIANT]
                self.game_metadata.players[self.my_color].name = player_info_config.get_value(player_info_config.Keys.OFFLINE_PLAYER_NAME)  # noqa: E501

                engine_name = "Fairy-Stockfish"
                engine_name = engine_name + f" Lvl {data.get(GameOption.COMPUTER_SKILL_LEVEL)}" if not data.get(GameOption.SPECIFY_ELO) else engine_name  # noqa: E501
                self.game_metadata.players[not self.my_color].name = engine_name
                self.game_metadata.players[not self.my_color].rating = data.get(GameOption.COMPUTER_ELO, "")

            self._notify_game_model_updated(*args, **kwargs)
        except KeyError as e:
            log.error(f"Error saving offline game metadata: {e}")

    def _report_game_over(self) -> None:
        """Saves game information and notifies listeners that the game has ended.
           This should only ever be called if the game is confirmed to be over
        """
        self.game_in_progress = False
        outcome = self.board_model.get_game_over_result()
        self.game_metadata.game_status.status = outcome.termination
        self.game_metadata.game_status.winner = COLOR_NAMES[outcome.winner]

        log.info(f"Game over (status={outcome.termination} winner={COLOR_NAMES[outcome.winner]})")
        self._notify_game_model_updated(EventTopics.GAME_END)
