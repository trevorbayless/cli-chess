from __future__ import annotations

import chess
from dataclasses import dataclass
from typing import FrozenSet, List, Optional, Set


@dataclass(frozen=True)
class MoveInputPreview:
    """Derived from the current board and a partial SAN string."""

    from_squares: FrozenSet[chess.Square]
    to_squares: FrozenSet[chess.Square]
    preview_move: Optional[chess.Move]


def _prefix_variants(partial: str) -> List[str]:
    """Allow castling to be typed with zero (0) instead of letter O."""
    p = partial.strip()
    if not p:
        return []
    alt = p.replace("0", "O")
    return [p] if alt == p else [p, alt]


def legal_moves_matching_san_prefix(board: chess.Board, partial: str) -> List[chess.Move]:
    """All legal moves whose SAN begins with partial (case-insensitive)."""
    variants = _prefix_variants(partial)
    if not variants:
        return []

    matches: List[chess.Move] = []
    for move in board.legal_moves:
        san_lower = board.san(move).lower()
        if any(san_lower.startswith(v.lower()) for v in variants):
            matches.append(move)
    return matches


def analyze_move_input(board: chess.Board, partial: str) -> MoveInputPreview:
    """Compute highlighted squares and a unique move, if the prefix resolves to one legal move."""
    moves = legal_moves_matching_san_prefix(board, partial)
    if not moves:
        return MoveInputPreview(frozenset(), frozenset(), None)

    from_squares: Set[chess.Square] = {m.from_square for m in moves}
    to_squares: Set[chess.Square] = {m.to_square for m in moves}
    preview: Optional[chess.Move] = moves[0] if len(moves) == 1 else None

    return MoveInputPreview(frozenset(from_squares), frozenset(to_squares), preview)


def longest_matching_san_prefix(board: chess.Board, partial: str) -> str:
    """Longest common prefix of SAN strings for moves matching partial (for Tab completion)."""
    moves = legal_moves_matching_san_prefix(board, partial)
    if not moves:
        return ""

    sans = sorted({board.san(m) for m in moves})
    first, last = sans[0], sans[-1]
    max_len = min(len(first), len(last))
    i = 0
    while i < max_len and first[i].lower() == last[i].lower():
        i += 1
    return first[:i]
