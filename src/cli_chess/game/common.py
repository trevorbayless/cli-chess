UNICODE_PIECE_SYMBOLS = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",
}

def get_piece_unicode_symbol(symbol: str) -> str:
    """Returns the unicode symbol associated to the symbol passed in"""
    unicode_symbol = ""
    symbol = symbol.lower()
    if symbol in UNICODE_PIECE_SYMBOLS:
        unicode_symbol = UNICODE_PIECE_SYMBOLS[symbol]

    return unicode_symbol