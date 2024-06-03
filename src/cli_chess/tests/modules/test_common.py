from cli_chess.modules.common import get_piece_unicode_symbol, UNICODE_PIECE_SYMBOLS
from string import ascii_lowercase


def test_get_piece_unicode_symbol():
    alphabet = list(ascii_lowercase)
    for letter in alphabet:
        if letter in UNICODE_PIECE_SYMBOLS:
            assert get_piece_unicode_symbol(letter) == UNICODE_PIECE_SYMBOLS[letter]
            assert get_piece_unicode_symbol(letter.upper()) == UNICODE_PIECE_SYMBOLS[letter]
        else:
            assert get_piece_unicode_symbol(letter) == ""
            assert get_piece_unicode_symbol(letter.upper()) == ""
    assert get_piece_unicode_symbol("") == ""
