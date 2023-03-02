# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
