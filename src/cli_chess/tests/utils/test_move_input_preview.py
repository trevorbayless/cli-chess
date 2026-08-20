import chess

from cli_chess.utils.move_input_preview import (
    analyze_move_input,
    legal_moves_matching_san_prefix,
    longest_matching_san_prefix,
)


def test_single_knight_prefix_identifies_one_square():
    board = chess.Board("8/8/8/8/8/8/8/N3K2k w - - 0 1")
    preview = analyze_move_input(board, "N")
    assert preview.from_squares == frozenset([chess.A1])
    assert preview.preview_move is None


def test_unique_move_sets_preview():
    board = chess.Board()
    preview = analyze_move_input(board, "e4")
    assert preview.preview_move is not None
    assert preview.preview_move == chess.Move.from_uci("e2e4")


def test_file_level_prefix_narrows_to_one_knight():
    board = chess.Board()
    nb_from = {m.from_square for m in legal_moves_matching_san_prefix(board, "Nc")}
    nf_from = {m.from_square for m in legal_moves_matching_san_prefix(board, "Nf")}
    assert nb_from == {chess.B1}
    assert nf_from == {chess.G1}


def test_castling_zero_for_letter_o():
    board = chess.Board("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    m_o = legal_moves_matching_san_prefix(board, "0-0")
    m_O = legal_moves_matching_san_prefix(board, "O-O")
    assert {m.uci() for m in m_o} == {m.uci() for m in m_O}


def test_longest_common_prefix_completion():
    board = chess.Board()
    assert longest_matching_san_prefix(board, "N") == "N"
    p = longest_matching_san_prefix(board, "e")
    assert p.startswith("e")


def test_no_match_returns_empty():
    board = chess.Board()
    preview = analyze_move_input(board, "Qzz")
    assert preview.from_squares == frozenset()
    assert longest_matching_san_prefix(board, "Qzz") == ""
