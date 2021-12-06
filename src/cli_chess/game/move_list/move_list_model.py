from cli_chess.game.board import BoardModel
from chess import Move, Board, piece_symbol, WHITE, BLACK
from typing import List

class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model

        # The board copy is used to generate the move list output
        # by using the move stack of the actual game on the board copy
        self.board_copy = BoardModel(variant=self.board_model.get_variant_name(),
                                     fen=self.board_model.get_initial_fen())


    def get_move_list_data(self) -> List[dict]:
        """Returns a list of dictionaries holding the move data"""
        move_list_data = []
        for move in self.board_model.get_move_stack():
            if not move:
                raise ValueError("Invalid move retrieved from move stack")

            color = WHITE if self.board_copy.board.turn == WHITE else BLACK
            san_move = self.board_copy.board.san_and_push(move)
            move_data = {'turn': color, 'move': san_move}

            move_list_data.append(move_data)

        self.board_copy.board.reset()
        return move_list_data