from __future__ import annotations

import os
import re
from datetime import datetime
from typing import TYPE_CHECKING, Optional

import chess

from cli_chess.utils.config import get_config_path
from cli_chess.utils.logging import log

if TYPE_CHECKING:
    from cli_chess.modules.board import BoardModel
    from cli_chess.core.game.game_metadata import GameMetadata


_STANDARD_START_FEN = chess.STARTING_FEN
_FILENAME_SAFE = re.compile(r"[^A-Za-z0-9._-]+")


def get_pgn_save_dir() -> str:
    return os.path.join(get_config_path(), "games")


def _slug(value: Optional[str], fallback: str) -> str:
    if not value:
        return fallback
    cleaned = _FILENAME_SAFE.sub("_", value).strip("_")
    return cleaned or fallback


def _player_name(metadata, color: chess.Color) -> str:
    player = metadata.players[color]
    name = player.name or "?"
    if player.title:
        return f"{player.title} {name}"
    return name


def _result_string(metadata) -> str:
    winner = metadata.game_status.winner
    status = metadata.game_status.status
    if winner == "white":
        return "1-0"
    if winner == "black":
        return "0-1"
    if status:
        return "1/2-1/2"
    return "*"


def _clock_seconds(value, units: str) -> Optional[int]:
    """Returns the passed in clock value in seconds. Berserk hands back clock
       durations as datetime objects (millis since the epoch), see berserk models.GameState
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return int(value.timestamp())
    return int(value // 1000) if units == "ms" else int(value)


def _time_control(metadata) -> Optional[str]:
    clock = metadata.clocks[chess.WHITE]
    base_seconds = _clock_seconds(clock.initial_time, clock.units)
    increment_seconds = _clock_seconds(clock.increment, clock.units)
    if base_seconds is None or increment_seconds is None:
        return None
    return f"{base_seconds}+{increment_seconds}"


def build_pgn_game(board_model: "BoardModel", metadata: "GameMetadata", is_online: bool):
    """Builds PGN from metadata"""
    import chess.pgn
    game = chess.pgn.Game.from_board(board_model.board)

    headers = game.headers
    headers["Event"] = "cli-chess online" if is_online else "cli-chess offline"
    headers["Site"] = f"lichess.org/{metadata.game_id}" if is_online and metadata.game_id else "local"
    headers["Date"] = datetime.now().strftime("%Y.%m.%d")
    headers["Round"] = "?"
    headers["White"] = _player_name(metadata, chess.WHITE)
    headers["Black"] = _player_name(metadata, chess.BLACK)
    headers["Result"] = _result_string(metadata)

    white_rating = metadata.players[chess.WHITE].rating
    black_rating = metadata.players[chess.BLACK].rating
    if white_rating:
        headers["WhiteElo"] = str(white_rating)
    if black_rating:
        headers["BlackElo"] = str(black_rating)

    tc = _time_control(metadata)
    headers["TimeControl"] = tc if tc else "-"

    variant = board_model.get_variant_name()
    if variant and variant != "chess":
        headers["Variant"] = variant

    if board_model.initial_fen and board_model.initial_fen != _STANDARD_START_FEN:
        headers["SetUp"] = "1"
        headers["FEN"] = board_model.initial_fen

    if metadata.game_status.status:
        headers["Termination"] = str(metadata.game_status.status)

    return game


def save_game_pgn(board_model: "BoardModel", metadata: "GameMetadata", is_online: bool) -> Optional[str]:
    """Creates PGN and returns full path of the file or none if no moves were present"""
    if not board_model.board.move_stack:
        log.debug("Skipping PGN save: no moves were played")
        return None

    try:
        import chess.pgn
        game = build_pgn_game(board_model, metadata, is_online)
        save_dir = get_pgn_save_dir()
        os.makedirs(save_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        white = _slug(metadata.players[chess.WHITE].name, "white")
        black = _slug(metadata.players[chess.BLACK].name, "black")
        filename = f"{timestamp}-{white}_vs_{black}.pgn"
        full_path = os.path.join(save_dir, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

        log.info(f"Saved game PGN to {full_path}")
        return full_path
    except Exception as e:
        log.error(f"Failed to save PGN: {e}")
        return None
