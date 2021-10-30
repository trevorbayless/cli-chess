from .board import Board

class GameModel:
    """ Business data. GameModel should have no knowledge of GameView
        or how this data will be used
    """
    def __init__(self):
        self.board = Board()


    def make_move(self, move):
        self.board.make_move(move)
