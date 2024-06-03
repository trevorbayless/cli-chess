UNICODE_PIECE_SYMBOLS = {
    "r": "♜",  # \u265C
    "n": "♞",  # \u265E
    "b": "♝",  # \u265D
    "q": "♛",  # \u265B
    "k": "♚",  # \u265A
    "p": "♙",  # \u2659 (avoid \u265F (♟) as it renders as emoji in most fonts)
}


def get_piece_unicode_symbol(symbol: str) -> str:
    """Returns the unicode symbol associated to the symbol passed in"""
    unicode_symbol = ""
    symbol = symbol.lower() if symbol else ""
    if symbol in UNICODE_PIECE_SYMBOLS:
        unicode_symbol = UNICODE_PIECE_SYMBOLS[symbol]

    return unicode_symbol
