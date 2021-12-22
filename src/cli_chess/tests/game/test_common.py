from cli_chess.game.common import *
from string import ascii_lowercase
import unittest

class CommonTestCase(unittest.TestCase):
    def test_get_piece_unicode_symbol(self):
        alphabet = list(ascii_lowercase)
        for letter in alphabet:
            if letter in UNICODE_PIECE_SYMBOLS:
                self.assertEqual(get_piece_unicode_symbol(letter), UNICODE_PIECE_SYMBOLS[letter])
                self.assertEqual(get_piece_unicode_symbol(letter.upper()), UNICODE_PIECE_SYMBOLS[letter])
            else:
                self.assertEqual(get_piece_unicode_symbol(letter), "")
                self.assertEqual(get_piece_unicode_symbol(letter.upper()), "")
        self.assertEqual(get_piece_unicode_symbol(""), "")
