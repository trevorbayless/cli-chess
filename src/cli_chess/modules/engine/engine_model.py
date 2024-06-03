from cli_chess.modules.board import BoardModel
from cli_chess.core.game.game_options import GameOption
from cli_chess.utils import log, is_linux_os, is_windows_os, is_mac_os
import chess.engine
from os import path
import platform
from typing import Optional


fairy_stockfish_mapped_skill_levels = {
    # These defaults are for the Fairy Stockfish engine
    # correlates levels 1-8 to a fairy-stockfish "equivalent"
    # This skill level mapping is to match Lichess' implementation
    1: -9,
    2: -5,
    3: -1,
    4: 3,
    5: 7,
    6: 11,
    7: 16,
    8: 20,
}


class EngineModel:
    def __init__(self, board_model: BoardModel, game_parameters: dict):
        self.engine: Optional[chess.engine.SimpleEngine] = None
        self.board_model = board_model
        self.game_parameters = game_parameters

    def start_engine(self):
        """Starts and configures the Fairy-Stockfish chess engine"""
        try:
            # Use SimpleEngine to allow engine assignment in initializer. Additionally,
            # by having this as a blocking call it stops multiple engines from being
            # able to be started if the start game button is spammed
            self.engine = chess.engine.SimpleEngine.popen_uci(path.dirname(path.realpath(__file__)) + "/binaries/" + self._get_engine_filename())

            # Engine configuration
            skill_level = fairy_stockfish_mapped_skill_levels.get(self.game_parameters.get(GameOption.COMPUTER_SKILL_LEVEL))
            limit_strength = self.game_parameters.get(GameOption.SPECIFY_ELO)
            uci_elo = self.game_parameters.get(GameOption.COMPUTER_ELO)
            engine_cfg = {
                'Skill Level': skill_level if skill_level else 0,
                'UCI_LimitStrength': True if limit_strength else False,
                'UCI_Elo': uci_elo if uci_elo else 1350
            }
            self.engine.configure(engine_cfg)
        except Exception as e:
            msg = f"Error starting engine: {e}"
            log.error(msg)
            raise Warning(msg)

    def get_best_move(self) -> chess.engine.PlayResult:
        """Query the engine to get the best move"""
        # Keep track of the last move that was made. This allows checking
        # for if a takeback happened while the engine has been thinking
        try:
            last_move = (self.board_model.get_move_stack() or [None])[-1]
            result = self.engine.play(self.board_model.board,
                                      chess.engine.Limit(2))

            # Check if the move stack has been altered, if so void this move
            if last_move != (self.board_model.get_move_stack() or [None])[-1]:
                result.move = None

            # Check to make sure the game is still in progress (opponent hasn't resigned)
            if self.board_model.get_game_over_result() is not None:
                result.move = None
        except Exception as e:
            log.error(f"{e}")
            if not self.engine:
                raise Warning("Engine is not running")
            raise

        log.debug(f"Returning {result}")
        return result

    def quit_engine(self) -> None:
        """Notify the engine to quit"""
        try:
            if self.engine:
                log.debug("Quitting engine")
                self.engine.quit()
        except Exception as e:
            log.error(f"Error quitting engine: {e}")

    @staticmethod
    def _get_engine_filename() -> str:
        """Returns the engines filename to use for opening"""
        binary_name = "fairy-stockfish_x86-64_" + ("linux" if is_linux_os() else ("windows" if is_windows_os() else "macos"))
        if is_mac_os() and platform.machine() == "arm64":
            binary_name = "fairy-stockfish_arm64_macos"
        return binary_name
